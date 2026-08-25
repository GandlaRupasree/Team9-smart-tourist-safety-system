from dotenv import load_dotenv
import os
from pymongo import MongoClient
import requests
import time

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def search_hotels(lat, lng, keyword="hotel"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 8000,
        "type": "lodging",
        "keyword": keyword,
        "key": API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        if data.get("status") == "OK":
            return data.get("results", [])
        else:
            return []
    except Exception as e:
        print(f"  error: {e}")
        return []

def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_address,formatted_phone_number,rating,price_level",
        "key": API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        if data.get("status") == "OK":
            return data.get("result", {})
    except Exception:
        pass
    return {}

destinations = list(db.destinations.find())
total = len(destinations)

db.real_hotels.delete_many({})

for i, dest in enumerate(destinations, 1):
    name = dest["name"]
    lat = dest["location"]["lat"]
    lng = dest["location"]["lng"]

    results = search_hotels(lat, lng)

    saved_count = 0
    for place in results[:6]:
        details = get_place_details(place.get("place_id", ""))
        hotel_doc = {
            "destination_name": name,
            "place_id": place.get("place_id"),
            "hotel_name": place.get("name"),
            "address": details.get("formatted_address", place.get("vicinity", "Address not available")),
            "phone": details.get("formatted_phone_number", "N/A"),
            "rating": place.get("rating", 0),
            "user_ratings_total": place.get("user_ratings_total", 0),
            "price_level": place.get("price_level", 2),
            "lat": place.get("geometry", {}).get("location", {}).get("lat"),
            "lng": place.get("geometry", {}).get("location", {}).get("lng")
        }
        db.real_hotels.insert_one(hotel_doc)
        saved_count += 1
        time.sleep(0.05)

    print(f"[{i}/{total}] {name} - saved {saved_count} real hotels", flush=True)
    time.sleep(0.1)

total_saved = db.real_hotels.count_documents({})
print(f"\nDONE. Total real hotels saved: {total_saved}")
