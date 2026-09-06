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
RADII_TO_TRY = [15000, 30000, 50000]
TARGET_COUNT = 5


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


def fetch_places(lat, lon, category, radius):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": category,
        "filter": f"circle:{lon},{lat},{radius}",
        "bias": f"proximity:{lon},{lat}",
        "limit": 10,
        "lang": "en",
        "apiKey": GEOAPIFY_KEY,
    }
    data = request_with_retry(url, params)
    return data.get("features", []) if data else []


def collect(lat, lon, category):
    results = []
    seen = set()
    for radius in RADII_TO_TRY:
        if len(results) >= TARGET_COUNT:
            break
        for f in fetch_places(lat, lon, category, radius):
            props = f.get("properties", {})
            name = props.get("name")
            if not name or name in seen:
                continue
            seen.add(name)
            results.append({
                "name": name,
                "address": props.get("formatted", ""),
                "phone": (props.get("contact") or {}).get("phone", "N/A"),
                "distance_km": round(props.get("distance", 0) / 1000, 1) if props.get("distance") else None,
                "lat": props.get("lat"),
                "lon": props.get("lon"),
            })
        time.sleep(0.3)
    return results


destinations = list(db.destinations.find({}))
total_hospitals = 0
total_police = 0

for i, dest in enumerate(destinations, start=1):
    location = dest.get("location", {})
    lat, lon = location.get("lat"), location.get("lng")
    if lat is None or lon is None:
        print(f"[{i}/{len(destinations)}] {dest.get('name')} - skipped, no coordinates")
        continue

    hospitals = collect(lat, lon, "healthcare.hospital")
    police = collect(lat, lon, "service.police")

    total_hospitals += len(hospitals)
    total_police += len(police)

    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"nearby_hospitals": hospitals, "nearby_police": police}}
    )
    print(f"[{i}/{len(destinations)}] {dest['name']} - {len(hospitals)} hospitals, {len(police)} police stations")
    time.sleep(0.2)

print(f"\nDONE. Total hospitals: {total_hospitals}. Total police stations: {total_police}.")
