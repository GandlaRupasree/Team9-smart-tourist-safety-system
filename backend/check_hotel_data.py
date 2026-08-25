from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

print("Total documents in real_hotels collection:", db.real_hotels.count_documents({}))
print()

for name in ["Chikmagalur", "Nagarhole", "Mysuru", "Coonoor"]:
    count = db.real_hotels.count_documents({"destination_name": name})
    print(f"{name}: {count} real hotels")
