from dotenv import load_dotenv
import os
import re
import time
import requests
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
CATEGORIES = "tourism.sights,tourism.attraction,heritage,natural.water,natural.mountain,leisure.park,entertainment.museum,religion.place_of_worship,memorial"
REQUEST_TIMEOUT = 25
MAX_RETRIES = 4
RADII_TO_TRY = [15000, 30000, 50000, 80000]
TARGET_COUNT = 15

# Only allow names in Latin script (covers English + common European accents).
# This filters out Hebrew, Kannada, Devanagari, etc. that slipped through
# because we didn't request a specific language before.
LATIN_ONLY = re.compile(r"^[A-Za-z0-9\u00C0-\u017F\s\-',.\&()/]+$")


def is_clean_name(name):
    return isinstance(name, str) and bool(name) and bool(LATIN_ONLY.match(name))


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


def fetch_attractions(lat, lon, radius):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": CATEGORIES,
        "filter": f"circle:{lon},{lat},{radius}",
        "bias": f"proximity:{lon},{lat}",
        "limit": 20,
        "lang": "en",
        "apiKey": GEOAPIFY_KEY,
    }
    data = request_with_retry(url, params)
    return data.get("features", []) if data else []


destinations = list(db.destinations.find({}))
total_removed = 0
total_added = 0

for i, dest in enumerate(destinations, start=1):
    existing = dest.get("real_attractions", [])
    cleaned = [a for a in existing if is_clean_name(a.get("name"))]
    removed = len(existing) - len(cleaned)
    total_removed += removed

    seen_names = {a["name"] for a in cleaned}
    location = dest.get("location", {})
    lat, lon = location.get("lat"), location.get("lng")

    added = 0
    if lat is not None and lon is not None and len(cleaned) < TARGET_COUNT:
        for radius in RADII_TO_TRY:
            if len(cleaned) >= TARGET_COUNT:
                break
            features = fetch_attractions(lat, lon, radius)
            for f in features:
                props = f.get("properties", {})
                name = props.get("name")
                if not name or name in seen_names or not is_clean_name(name):
                    continue
                seen_names.add(name)
                cleaned.append({
                    "name": name,
                    "category": (props.get("categories") or ["tourism.sights"])[0],
                })
                added += 1
            time.sleep(0.3)

    total_added += added
    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"real_attractions": cleaned}}
    )
    print(f"[{i}/{len(destinations)}] {dest['name']} - removed {removed} non-Latin, added {added}, now has {len(cleaned)}")
    time.sleep(0.2)

print(f"\nDONE. Total removed: {total_removed}. Total added: {total_added}.")
