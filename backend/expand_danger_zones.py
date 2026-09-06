from dotenv import load_dotenv
import os
import time
import requests
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
REQUEST_TIMEOUT = 25
MAX_RETRIES = 4
RADII_TO_TRY = [20000, 40000, 70000]


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


def fetch(lat, lon, category, radius, limit=3):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": category,
        "filter": f"circle:{lon},{lat},{radius}",
        "bias": f"proximity:{lon},{lat}",
        "limit": limit,
        "lang": "en",
        "apiKey": GEOAPIFY_KEY,
    }
    data = request_with_retry(url, params)
    results = []
    if data:
        for f in data.get("features", []):
            props = f.get("properties", {})
            name = props.get("name")
            if not name:
                continue
            results.append({"name": name, "lat": props.get("lat"), "lng": props.get("lon")})
    return results


def fetch_with_widening_radius(lat, lon, category, seen_names):
    for radius in RADII_TO_TRY:
        results = [r for r in fetch(lat, lon, category, radius) if r["name"] not in seen_names]
        if results:
            return results
        time.sleep(0.2)
    return []


destinations = list(db.destinations.find({}))
total_danger = 0
newly_covered = 0

for i, dest in enumerate(destinations, start=1):
    location = dest.get("location", {})
    lat, lon = location.get("lat"), location.get("lng")
    if lat is None or lon is None:
        print(f"[{i}/{len(destinations)}] {dest.get('name')} - skipped, no coordinates")
        continue

    existing = dest.get("danger_zones", [])
    seen = {d["name"] for d in existing}

    military = fetch_with_widening_radius(lat, lon, "building.military", seen)
    seen.update(d["name"] for d in military)
    time.sleep(0.2)

    cliffs = fetch_with_widening_radius(lat, lon, "natural.mountain.cliff", seen)
    seen.update(d["name"] for d in cliffs)
    time.sleep(0.2)

    rapids = fetch_with_widening_radius(lat, lon, "natural.water.whitewater", seen)
    time.sleep(0.2)

    combined = existing + military + cliffs + rapids
    if len(combined) > len(existing):
        newly_covered += 1

    total_danger += len(combined)
    db.destinations.update_one({"_id": dest["_id"]}, {"$set": {"danger_zones": combined}})
    print(f"[{i}/{len(destinations)}] {dest['name']} - now has {len(combined)} danger zones ({len(military)} military, {len(cliffs)} cliffs, {len(rapids)} rapids found this run)")

print(f"\nDONE. {newly_covered} destinations gained new danger zones. Total danger zones now: {total_danger}.")
