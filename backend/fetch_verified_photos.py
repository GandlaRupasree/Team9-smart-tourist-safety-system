from dotenv import load_dotenv
import os
import time
import requests
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

WIKI_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "TourSafeStudentProject/1.0 (contact: student-project@example.com)"}
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3


def request_with_retry(params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(WIKI_URL, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"      attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)
    return None


def wiki_thumbnail(search_query):
    search_params = {
        "action": "query", "list": "search", "srsearch": search_query,
        "format": "json", "srlimit": 1,
    }
    search_data = request_with_retry(search_params)
    if not search_data:
        return None
    results = search_data.get("query", {}).get("search", [])
    if not results:
        return None
    title = results[0]["title"]

    image_params = {
        "action": "query", "titles": title, "prop": "pageimages",
        "format": "json", "pithumbsize": 600,
    }
    image_data = request_with_retry(image_params)
    if not image_data:
        return None
    pages = image_data.get("query", {}).get("pages", {})
    for page in pages.values():
        thumb = page.get("thumbnail", {})
        if thumb.get("source"):
            return thumb["source"]
    return None


def find_wiki_photo_with_fallback(attraction_name, destination_name):
    # Try the combined query first, then fall back to the attraction name alone
    img = wiki_thumbnail(f"{attraction_name} {destination_name}")
    if img:
        return img
    return wiki_thumbnail(attraction_name)


destinations = list(db.destinations.find({}))
dest_photos_found = 0
attr_photos_found = 0

for i, dest in enumerate(destinations, start=1):
    name = dest["name"]

    # 1. Verified destination-level photo (replaces the unreliable seed real_image_url)
    verified_url = wiki_thumbnail(f"{name} India") or wiki_thumbnail(name)
    if verified_url:
        dest_photos_found += 1
    time.sleep(0.2)

    # 2. Attraction photos with fallback search
    attractions = dest.get("attractions", [])
    photos = []
    for attraction in attractions:
        try:
            img = find_wiki_photo_with_fallback(attraction, name)
        except Exception as e:
            print(f"      error on '{attraction}': {e}")
            img = None
        if img:
            attr_photos_found += 1
        photos.append({"name": attraction, "image_url": img})
        time.sleep(0.2)

    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"verified_image_url": verified_url, "attraction_photos": photos}}
    )

    found_count = sum(1 for p in photos if p["image_url"])
    print(f"[{i}/{len(destinations)}] {name} - dest photo: {'yes' if verified_url else 'no'}, attractions: {found_count}/{len(attractions)}")

print(f"\nDONE. Destination photos found: {dest_photos_found}/{len(destinations)}. Attraction photos found: {attr_photos_found}.")
