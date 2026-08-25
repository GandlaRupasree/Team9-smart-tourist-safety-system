from dotenv import load_dotenv
import os
import random
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

type_multiplier = {
    "hotel": 1.0,
    "resort": 1.4,
    "homestay": 0.5,
    "hostel": 0.35,
    "motel": 0.6,
}

hotels = list(db.real_hotels.find({"estimated_price_per_night": {"$exists": False}}))
updated = 0

for hotel in hotels:
    dest = db.destinations.find_one({"name": hotel["destination_name"]})
    base_cost = dest["avg_cost"] if dest else 2000
    mult = type_multiplier.get(hotel.get("tourism_type", "hotel"), 1.0)
    price = round(base_cost * mult * random.uniform(0.8, 1.2))
    rating = round(random.uniform(3.6, 4.8), 1)

    db.real_hotels.update_one(
        {"_id": hotel["_id"]},
        {"$set": {"estimated_price_per_night": price, "rating": rating}}
    )
    updated += 1

print(f"Added pricing to {updated} real hotels")
