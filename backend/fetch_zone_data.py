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
RADIUS = 20000


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


def fetch(lat, lon, category, limit=5):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": category,
        "filter": f"circle:{lon},{lat},{RADIUS}",
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


destinations = list(db.destinations.find({}))
total_warning = 0
total_danger = 0

for i, dest in enumerate(destinations, start=1):
    location = dest.get("location", {})
    lat, lon = location.get("lat"), location.get("lng")
    if lat is None or lon is None:
        print(f"[{i}/{len(destinations)}] {dest.get('name')} - skipped, no coordinates")
        continue

    forests = fetch(lat, lon, "natural.forest", limit=3)
    time.sleep(0.2)
    protected = fetch(lat, lon, "natural.protected_area", limit=3)
    time.sleep(0.2)
    military = fetch(lat, lon, "building.military", limit=2)
    time.sleep(0.2)

    warning = forests + protected
    danger = military

    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"warning_zones": warning, "danger_zones": danger}}
    )
    total_warning += len(warning)
    total_danger += len(danger)
    print(f"[{i}/{len(destinations)}] {dest['name']} - {len(warning)} warning, {len(danger)} danger zones")

print(f"\nDONE. Total warning zones: {total_warning}. Total danger zones: {total_danger}.")
