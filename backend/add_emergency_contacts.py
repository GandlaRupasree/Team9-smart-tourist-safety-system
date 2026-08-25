from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

state_emergency_numbers = {
    "default": {"police": "100", "ambulance": "108", "tourist_helpline": "1363", "fire": "101"}
}

destinations = list(db.destinations.find())
updated = 0
for dest in destinations:
    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"emergency_contacts": state_emergency_numbers["default"]}}
    )
    updated += 1

print(f"Added emergency contacts to {updated} destinations")
