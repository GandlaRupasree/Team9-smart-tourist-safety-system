from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

print("Hostels remaining:", db.real_hotels.count_documents({"tourism_type": "hostel"}))
print("Total real hotels:", db.real_hotels.count_documents({}))
print("By type:")
for t in ["hotel", "resort", "homestay"]:
    print(f"  {t}: {db.real_hotels.count_documents({'tourism_type': t})}")
