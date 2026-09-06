from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

dest = db.destinations.find_one({"name": "Coorg"})
print("verified_image_url:", dest.get("verified_image_url"))
print("real_attractions count:", len(dest.get("real_attractions", [])))
print("attraction_photos count:", len(dest.get("attraction_photos", [])))

print("\nreal_hotels total:", db.real_hotels.count_documents({}))
print("destinations total:", db.destinations.count_documents({}))
print("accommodations total:", db.accommodations.count_documents({}))
