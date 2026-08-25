from dotenv import load_dotenv
import os
import time
import requests
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
CATEGORIES = "accommodation.hotel,accommodation.guest_house,accommodation.motel"
REQUEST_TIMEOUT = 25
MAX_RETRIES = 4

# Widening radii to try in order - many of these are remote/rural spots
# (national parks, deserts, wildlife sanctuaries) where the nearest real
# lodging may sit further out than the 10km used for the main run.
RADII_TO_TRY = [10000, 20000, 35000, 50000]

FALLBACK_IMAGES = {
    "hotel": "https://loremflickr.com/400/300/hotel,building",
    "resort": "https://loremflickr.com/400/300/resort,pool",
    "homestay": "https://loremflickr.com/400/300/homestay,cottage",
}


def request_with_retry(url, params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"      attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)
    return None


def lodging_type(categories, name):
    name_l = (name or "").lower()
    if "resort" in name_l:
        return "resort"
    if "accommodation.guest_house" in categories:
        return "homestay"
    if "accommodation.motel" in categories:
        return "homestay"
    return "hotel"


def fetch_photo(place_id):
    if not place_id:
        return None
    url = "https://api.geoapify.com/v2/place-details"
    params = {"id": place_id, "features": "wiki_and_media", "apiKey": GEOAPIFY_KEY}
    data = request_with_retry(url, params)
    if not data:
        return None
    try:
        props = data["features"][0]["properties"]
        return props.get("wiki_and_media", {}).get("image")
    except (KeyError, IndexError):
        return None


def fetch_lodging(lat, lon, radius):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": CATEGORIES,
        "filter": f"circle:{lon},{lat},{radius}",
        "bias": f"proximity:{lon},{lat}",
        "limit": 20,
        "apiKey": GEOAPIFY_KEY,
    }
    data = request_with_retry(url, params)
    return data.get("features", []) if data else []


def upsert_hotel(destination_name, feature):
    props = feature.get("properties", {})
    place_id = props.get("place_id")
    if not place_id or db.real_hotels.find_one({"place_id": place_id}):
        return False

    name = props.get("name") or "Unnamed Lodging"
    categories = props.get("categories", [])
    ltype = lodging_type(categories, name)
    contact = props.get("contact", {}) or {}
    image_url = fetch_photo(place_id) or FALLBACK_IMAGES.get(ltype, FALLBACK_IMAGES["hotel"])

    db.real_hotels.insert_one({
        "hotel_name": name,
        "destination_name": destination_name,
        "tourism_type": ltype,
        "address": props.get("formatted", "Address not available"),
        "phone": contact.get("phone", "N/A"),
        "website": contact.get("website"),
        "latitude": props.get("lat"),
        "longitude": props.get("lon"),
        "image_url": image_url,
        "place_id": place_id,
        "source": "geoapify",
    })
    return True


ZERO_RESULT_DESTINATIONS = [
    "Andaman Islands", "Rann of Kutch", "Araku Valley", "Kaziranga", "Sundarbans",
    "Sasan Gir", "Halebidu", "Pandharpur", "Netarhat", "Betla", "Nalanda",
    "Rajgir", "Amaravati", "Chilika Lake", "Similipal",
]

for i, name in enumerate(ZERO_RESULT_DESTINATIONS, start=1):
    dest = db.destinations.find_one({"name": name})
    if not dest:
        print(f"[{i}/{len(ZERO_RESULT_DESTINATIONS)}] {name} - not found in destinations collection")
        continue

    location = dest.get("location", {})
    lat, lon = location.get("lat"), location.get("lng")
    if lat is None or lon is None:
        print(f"[{i}/{len(ZERO_RESULT_DESTINATIONS)}] {name} - no coordinates on this doc")
        continue

    saved_total = 0
    for radius in RADII_TO_TRY:
        features = fetch_lodging(lat, lon, radius)
        saved = sum(1 for f in features if upsert_hotel(name, f))
        saved_total += saved
        if saved_total > 0:
            print(f"[{i}/{len(ZERO_RESULT_DESTINATIONS)}] {name} - saved {saved_total} lodgings at radius {radius/1000:.0f}km")
            break
        time.sleep(0.3)
    else:
        print(f"[{i}/{len(ZERO_RESULT_DESTINATIONS)}] {name} - still 0 lodgings even at {RADII_TO_TRY[-1]/1000:.0f}km (genuinely no OSM data nearby)")

    time.sleep(0.3)

print("\nDone retrying zero-result destinations.")
