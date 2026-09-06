from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

FALLBACK_IMAGES = {
    "hotel": "https://loremflickr.com/400/300/hotel,building",
    "hostel": "https://loremflickr.com/400/300/hostel,dorm",
    "resort": "https://loremflickr.com/400/300/resort,pool",
    "homestay": "https://loremflickr.com/400/300/homestay,cottage",
    "motel": "https://loremflickr.com/400/300/motel",
}

broken = list(db.real_hotels.find({"image_url": {"$regex": "source.unsplash.com"}}))
updated = 0

for hotel in broken:
    ltype = hotel.get("tourism_type", "hotel")
    new_url = FALLBACK_IMAGES.get(ltype, FALLBACK_IMAGES["hotel"])
    db.real_hotels.update_one({"_id": hotel["_id"]}, {"$set": {"image_url": new_url}})
    updated += 1

print(f"Fixed {updated} broken image URLs")
