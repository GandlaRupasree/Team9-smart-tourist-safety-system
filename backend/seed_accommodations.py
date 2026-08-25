from dotenv import load_dotenv
import os
from pymongo import MongoClient
import random

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

db.accommodations.delete_many({})

destinations = list(db.destinations.find())

name_templates = {
    "Hotel": ["{} Grand Hotel", "{} Comfort Inn", "{} Regency", "Hotel {} Palace", "{} City Hotel"],
    "Hostel": ["{} Backpackers Hostel", "{} Zostel", "{} Travellers Nest", "{} Bunk House"],
    "Resort": ["{} Hills Resort", "{} Lake Resort", "{} Paradise Resort", "{} Retreat Resort"],
    "Homestay": ["{} Heritage Homestay", "{} Family Homestay", "{} Cozy Cottage", "{} Local Homestay"]
}

base_price = {"Hostel": 500, "Homestay": 900, "Hotel": 1800, "Resort": 3500}
price_variance = {"Hostel": 300, "Homestay": 500, "Hotel": 1200, "Resort": 2500}

accommodations = []
for dest in destinations:
    for acc_type, templates in name_templates.items():
        num_options = random.randint(2, 3)
        chosen_templates = random.sample(templates, min(num_options, len(templates)))
        for template in chosen_templates:
            price = base_price[acc_type] + random.randint(0, price_variance[acc_type])
            accommodations.append({
                "destination_name": dest["name"],
                "type": acc_type,
                "name": template.format(dest["name"]),
                "price_per_night": price,
                "rating": round(random.uniform(3.5, 4.9), 1),
                "amenities": random.sample(
                    ["Free WiFi", "AC", "Breakfast Included", "Parking", "Pool", "Room Service", "24hr Front Desk"],
                    k=random.randint(3, 5)
                )
            })

result = db.accommodations.insert_many(accommodations)
print(f"Inserted {len(result.inserted_ids)} accommodation listings for {len(destinations)} destinations")

missing_check = []
for dest in destinations:
    for acc_type in name_templates.keys():
        count = db.accommodations.count_documents({"destination_name": dest["name"], "type": acc_type})
        if count == 0:
            missing_check.append(f"{dest['name']} - {acc_type}")

if missing_check:
    print(f"WARNING: {len(missing_check)} destination/type combos still missing:")
    for m in missing_check[:10]:
        print(f"  - {m}")
else:
    print("Confirmed: every destination has at least one listing for every accommodation type.")
