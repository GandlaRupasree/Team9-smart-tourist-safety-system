from dotenv import load_dotenv
import os
import re
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

LATIN_ONLY = re.compile(r"^[A-Za-z0-9\u00C0-\u017F\s\-',.\&()/]+$")

def is_clean_name(name):
    return isinstance(name, str) and bool(name) and bool(LATIN_ONLY.match(name))

destinations = list(db.destinations.find({}))
total_removed = 0
destinations_affected = 0

for dest in destinations:
    existing = dest.get("real_attractions", [])
    cleaned = [a for a in existing if is_clean_name(a.get("name"))]
    removed = len(existing) - len(cleaned)

    if removed > 0:
        total_removed += removed
        destinations_affected += 1
        db.destinations.update_one({"_id": dest["_id"]}, {"$set": {"real_attractions": cleaned}})
        print(f"{dest['name']} - removed {removed} non-Latin entries, now has {len(cleaned)}")

print(f"\nDONE. {destinations_affected} destinations had leftover non-Latin names, {total_removed} entries removed total.")
