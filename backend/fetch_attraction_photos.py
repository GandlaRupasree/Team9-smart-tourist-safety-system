from dotenv import load_dotenv
import os
import time
import requests
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3


def request_with_retry(params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(WIKI_SEARCH_URL, params=params, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"      attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)
    return None


def find_wiki_photo(attraction_name, destination_name):
    # Search Wikipedia for the best matching page (include destination for disambiguation)
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": f"{attraction_name} {destination_name}",
        "format": "json",
        "srlimit": 1,
    }
    search_data = request_with_retry(search_params)
    if not search_data:
        return None
    results = search_data.get("query", {}).get("search", [])
    if not results:
        return None
    title = results[0]["title"]

    # Get the page's thumbnail image
    image_params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 600,
    }
    image_data = request_with_retry(image_params)
    if not image_data:
        return None
    pages = image_data.get("query", {}).get("pages", {})
    for page in pages.values():
        thumbnail = page.get("thumbnail", {})
        if thumbnail.get("source"):
            return {"image_url": thumbnail["source"], "wiki_title": title}
    return None


def main():
    destinations = list(db.destinations.find({}))
    total_photos = 0

    for i, dest in enumerate(destinations, start=1):
        attractions = dest.get("attractions", [])
        if not attractions:
            print(f"[{i}/{len(destinations)}] {dest['name']} - no attractions listed, skipped")
            continue

        photos = []
        for attraction in attractions:
            try:
                result = find_wiki_photo(attraction, dest["name"])
            except Exception as e:
                print(f"      error on '{attraction}': {e}")
                result = None

            if result:
                photos.append({"name": attraction, "image_url": result["image_url"]})
            else:
                photos.append({"name": attraction, "image_url": None})
            time.sleep(0.2)

        db.destinations.update_one({"_id": dest["_id"]}, {"$set": {"attraction_photos": photos}})
        found = sum(1 for p in photos if p["image_url"])
        total_photos += found
        print(f"[{i}/{len(destinations)}] {dest['name']} - found photos for {found}/{len(attractions)} attractions")

    print(f"\nDONE. Total attraction photos found: {total_photos}")


if __name__ == "__main__":
    main()
