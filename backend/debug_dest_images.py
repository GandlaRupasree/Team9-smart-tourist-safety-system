from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

for name in ["Mysuru", "Nagarhole", "Coimbatore", "Coorg", "Lepakshi"]:
    dest = db.destinations.find_one({"name": name})
    if not dest:
        print(f"{name}: NOT FOUND")
        continue
    print(f"\n{name}")
    print("  real_image_url:", dest.get("real_image_url"))
    photos = dest.get("attraction_photos")
    if photos is None:
        print("  attraction_photos: field missing entirely")
    else:
        for p in photos:
            print(f"    - {p.get('name')}: {p.get('image_url')}")
