from dotenv import load_dotenv
import os
from pymongo import MongoClient
import random

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

destinations = list(db.destinations.find())
updated = 0
for dest in destinations:
    radius_km = round(random.uniform(3, 8), 1)
    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"safe_zone_radius_km": radius_km}}
    )
    updated += 1

print(f"Added safe zone radius to {updated} destinations")
