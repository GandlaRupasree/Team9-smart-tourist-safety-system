from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

EXCLUDE_KEYWORDS = ["veterinary", "vet clinic", "animal hospital", "pet hospital", "pashu"]

def is_human_hospital(name):
    name_lower = (name or "").lower()
    return not any(kw in name_lower for kw in EXCLUDE_KEYWORDS)

destinations = list(db.destinations.find({"nearby_hospitals": {"$exists": True}}))
total_removed = 0
affected = 0

for dest in destinations:
    hospitals = dest.get("nearby_hospitals", [])
    filtered = [h for h in hospitals if is_human_hospital(h.get("name"))]
    removed = len(hospitals) - len(filtered)
    if removed > 0:
        total_removed += removed
        affected += 1
        db.destinations.update_one({"_id": dest["_id"]}, {"$set": {"nearby_hospitals": filtered}})
        print(f"{dest['name']} - removed {removed} veterinary/animal entries")

print(f"\nDONE. {affected} destinations affected, {total_removed} entries removed total.")
