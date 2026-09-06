from dotenv import load_dotenv
import os
from pymongo import MongoClient
import requests
import time
import sys

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

def get_wikipedia_image(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        resp = requests.get(url, timeout=4, headers={"User-Agent": "TourSafeApp/1.0"})
        if resp.status_code == 200:
            data = resp.json()
            if "thumbnail" in data and "source" in data["thumbnail"]:
                return data["thumbnail"]["source"]
    except Exception:
        pass
    return None

destinations = list(db.destinations.find())
total = len(destinations)
updated = 0
skipped = 0
failed = []

for i, dest in enumerate(destinations, 1):
    name = dest["name"]

    if dest.get("real_image_url") or dest.get("image_fetch_attempted"):
        skipped += 1
        print(f"[{i}/{total}] {name} - already processed, skipping", flush=True)
        continue

    attractions = dest.get("attractions", [])
    search_terms = [attractions[0], name] if attractions else [name]

    image_url = None
    for term in search_terms:
        image_url = get_wikipedia_image(term)
        if image_url:
            break

    if image_url:
        db.destinations.update_one(
            {"_id": dest["_id"]},
            {"$set": {"real_image_url": image_url, "image_source_place": search_terms[0], "image_fetch_attempted": True}}
        )
        updated += 1
        print(f"[{i}/{total}] {name} - FOUND image", flush=True)
    else:
        db.destinations.update_one({"_id": dest["_id"]}, {"$set": {"image_fetch_attempted": True}})
        failed.append(name)
        print(f"[{i}/{total}] {name} - no image found", flush=True)

print(f"\nDONE. Found real images for {updated} destinations this run.")
print(f"Skipped {skipped} already-processed destinations.")
print(f"No image found for {len(failed)} destinations (will use fallback).")
