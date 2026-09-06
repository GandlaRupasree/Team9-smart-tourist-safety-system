from dotenv import load_dotenv
import os
import time
import requests
from pymongo import MongoClient

load_dotenv()

GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

CATEGORIES = "accommodation.hotel,accommodation.guest_house,accommodation.motel"
RADIUS_METERS = 10000
REQUEST_TIMEOUT = 20
MAX_RETRIES = 3

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
            print(f"    attempt {attempt}/{MAX_RETRIES} failed: {e}")
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
    """Try a real Wikimedia photo via Place Details. Returns None if OSM/Wikimedia has none."""
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


def fetch_lodging(lat, lon):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": CATEGORIES,
        "filter": f"circle:{lon},{lat},{RADIUS_METERS}",
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


def main():
    if not GEOAPIFY_KEY:
        raise SystemExit("GEOAPIFY_API_KEY missing from .env - get a free key at https://myprojects.geoapify.com/")

    destinations = list(db.destinations.find({}))
    total_saved = 0

    for i, dest in enumerate(destinations, start=1):
        location = dest.get("location", {})
        lat, lon = location.get("lat"), location.get("lng")
        if lat is None or lon is None:
            print(f"[{i}/{len(destinations)}] {dest.get('name')} - skipped, no location.lat/lng on this doc")
            continue

        try:
            features = fetch_lodging(lat, lon)
            saved = sum(1 for f in features if upsert_hotel(dest["name"], f))
            total_saved += saved
            print(f"[{i}/{len(destinations)}] {dest['name']} - saved {saved} lodgings")
        except Exception as e:
            print(f"[{i}/{len(destinations)}] {dest['name']} - SKIPPED due to error: {e}")
        time.sleep(0.3)

    print(f"\nDONE. Total lodgings saved: {total_saved}")


if __name__ == "__main__":
    main()







