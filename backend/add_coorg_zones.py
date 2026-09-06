import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

zones_data = {
    "zones": [
        {
            "type": "safe",
            "label": "Madikeri City Center",
            "lat": 12.3375,
            "lng": 75.8069,
            "radius_km": 3,
            "details": {
                "crime_rate": "Low",
                "note": "2 stations nearby"
            }
        },
        {
            "type": "warning",
            "label": "Construction Zone",
            "lat": 12.3550,
            "lng": 75.8200,
            "radius_km": 1,
            "details": {
                "reason": "Road work in progress",
                "advice": "Use alternate routes, expect delays"
            }
        },
        {
            "type": "danger",
            "label": "Restricted Military Area",
            "lat": 12.3100,
            "lng": 75.7900,
            "radius_km": 1.5,
            "details": {
                "reason": "Entry prohibited",
                "advice": "Avoid this area completely"
            }
        }
    ],
    "emergency_contacts": {
        "police": "100",
        "ambulance": "108",
        "fire": "101",
        "tourist_helpline": "1363"
    }
}

result = db.destinations.update_one(
    {"name": "Coorg"},
    {"$set": zones_data}
)

print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")
