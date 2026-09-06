from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["toursafe"]

print("Connected to database:", db.name)
print("Collections in this database:", db.list_collection_names())
print()
print("destinations count:", db.destinations.count_documents({}))
print("real_hotels count:", db.real_hotels.count_documents({}))
print("accommodations count:", db.accommodations.count_documents({}))
print("bookings count:", db.bookings.count_documents({}))
print()
print("MONGO_URI (partially masked):", uri[:20] + "..." + uri[-20:] if uri else "NOT SET")
