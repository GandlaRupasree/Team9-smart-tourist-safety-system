from dotenv import load_dotenv
import os
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
        "apiKey": GEOAPIFY_KEY,
    }
    data = request_with_retry(url, params)
    return data.get("features", []) if data else []


destinations = list(db.destinations.find({}))
total_added = 0

for i, dest in enumerate(destinations, start=1):
    location = dest.get("location", {})
    lat, lon = location.get("lat"), location.get("lng")
    if lat is None or lon is None:
        print(f"[{i}/{len(destinations)}] {dest.get('name')} - skipped, no coordinates")
        continue

    existing = dest.get("real_attractions", [])
    seen_names = {a["name"] for a in existing}
    real_attractions = list(existing)

    for radius in RADII_TO_TRY:
        if len(real_attractions) >= TARGET_COUNT:
            break
        features = fetch_attractions(lat, lon, radius)
        for f in features:
            props = f.get("properties", {})
            name = props.get("name")
            if not name or name in seen_names:
                continue
            seen_names.add(name)
            real_attractions.append({
                "name": name,
                "category": (props.get("categories") or ["tourism.sights"])[0],
            })
        time.sleep(0.3)

    added = len(real_attractions) - len(existing)
    total_added += added
    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"real_attractions": real_attractions}}
    )
    print(f"[{i}/{len(destinations)}] {dest['name']} - now has {len(real_attractions)} real attractions (+{added})")
    time.sleep(0.3)

print(f"\nDONE. Total new attractions added: {total_added}")
