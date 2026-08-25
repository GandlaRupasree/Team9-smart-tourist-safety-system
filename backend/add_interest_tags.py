from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

interest_map = {
    "Coorg": {"interests": ["Nature", "Adventure"], "min_days": 2, "max_days": 4},
    "Hampi": {"interests": ["Historical Places", "Adventure"], "min_days": 2, "max_days": 3},
    "Chikmagalur": {"interests": ["Nature", "Adventure"], "min_days": 2, "max_days": 4},
    "Gokarna": {"interests": ["Beaches", "Nature"], "min_days": 2, "max_days": 4},
    "Mysuru": {"interests": ["Historical Places", "Shopping"], "min_days": 1, "max_days": 3},
    "Ooty": {"interests": ["Nature"], "min_days": 2, "max_days": 4},
    "Wayanad": {"interests": ["Nature", "Wildlife", "Adventure"], "min_days": 2, "max_days": 4},
    "Pondicherry": {"interests": ["Beaches", "Historical Places"], "min_days": 2, "max_days": 3},
    "Munnar": {"interests": ["Nature"], "min_days": 2, "max_days": 4},
    "Bandipur": {"interests": ["Wildlife", "Nature"], "min_days": 1, "max_days": 2},

    "Jaipur": {"interests": ["Historical Places", "Shopping"], "min_days": 2, "max_days": 4},
    "Udaipur": {"interests": ["Historical Places", "Nature"], "min_days": 2, "max_days": 3},
    "Jaisalmer": {"interests": ["Historical Places", "Adventure"], "min_days": 2, "max_days": 3},
    "Jodhpur": {"interests": ["Historical Places", "Shopping"], "min_days": 2, "max_days": 3},

    "Manali": {"interests": ["Adventure", "Nature"], "min_days": 3, "max_days": 6},
    "Shimla": {"interests": ["Nature"], "min_days": 2, "max_days": 4},
    "Dharamshala": {"interests": ["Nature", "Religious Tourism", "Adventure"], "min_days": 2, "max_days": 4},

    "Rishikesh": {"interests": ["Adventure", "Religious Tourism", "Nature"], "min_days": 2, "max_days": 4},
    "Nainital": {"interests": ["Nature"], "min_days": 2, "max_days": 3},

    "Agra": {"interests": ["Historical Places"], "min_days": 1, "max_days": 2},
    "Varanasi": {"interests": ["Religious Tourism", "Historical Places"], "min_days": 2, "max_days": 3},

    "Darjeeling": {"interests": ["Nature"], "min_days": 3, "max_days": 5},

    "Goa": {"interests": ["Beaches", "Adventure", "Shopping"], "min_days": 3, "max_days": 6},

    "Alleppey": {"interests": ["Nature", "Beaches"], "min_days": 2, "max_days": 3},
    "Kochi": {"interests": ["Historical Places", "Shopping"], "min_days": 1, "max_days": 2},

    "Kodaikanal": {"interests": ["Nature"], "min_days": 2, "max_days": 4},
    "Madurai": {"interests": ["Religious Tourism", "Historical Places"], "min_days": 1, "max_days": 2},

    "Andaman Islands": {"interests": ["Beaches", "Adventure"], "min_days": 4, "max_days": 7},

    "Leh Ladakh": {"interests": ["Adventure", "Nature"], "min_days": 5, "max_days": 10},

    "Ranthambore": {"interests": ["Wildlife", "Adventure"], "min_days": 2, "max_days": 3},

    "Mumbai": {"interests": ["Shopping", "Historical Places"], "min_days": 2, "max_days": 4},

    "Amritsar": {"interests": ["Religious Tourism", "Historical Places"], "min_days": 1, "max_days": 2},

    "Shillong": {"interests": ["Nature", "Adventure"], "min_days": 3, "max_days": 5},

    "Khajuraho": {"interests": ["Historical Places"], "min_days": 1, "max_days": 2},
    "Bhopal": {"interests": ["Historical Places", "Nature"], "min_days": 2, "max_days": 3},

    "Rann of Kutch": {"interests": ["Adventure", "Nature"], "min_days": 2, "max_days": 4},
    "Somnath": {"interests": ["Religious Tourism"], "min_days": 1, "max_days": 2},

    "Puri": {"interests": ["Religious Tourism", "Beaches"], "min_days": 2, "max_days": 3},
    "Konark": {"interests": ["Historical Places", "Beaches"], "min_days": 1, "max_days": 2},

    "Tirupati": {"interests": ["Religious Tourism"], "min_days": 1, "max_days": 2},
    "Araku Valley": {"interests": ["Nature"], "min_days": 2, "max_days": 3},

    "Hyderabad": {"interests": ["Historical Places", "Shopping"], "min_days": 2, "max_days": 3},

    "Gangtok": {"interests": ["Nature", "Adventure"], "min_days": 3, "max_days": 5},

    "Srinagar": {"interests": ["Nature", "Adventure"], "min_days": 3, "max_days": 6},
    "Gulmarg": {"interests": ["Adventure", "Nature"], "min_days": 2, "max_days": 4},

    "Lonavala": {"interests": ["Nature"], "min_days": 1, "max_days": 2},
    "Mahabaleshwar": {"interests": ["Nature"], "min_days": 2, "max_days": 3},
    "Ajanta Ellora": {"interests": ["Historical Places"], "min_days": 1, "max_days": 2},

    "Kaziranga": {"interests": ["Wildlife", "Nature"], "min_days": 2, "max_days": 3},

    "Bodh Gaya": {"interests": ["Religious Tourism", "Historical Places"], "min_days": 1, "max_days": 2},

    "Kolkata": {"interests": ["Historical Places", "Shopping"], "min_days": 2, "max_days": 4},
    "Sundarbans": {"interests": ["Wildlife", "Nature", "Adventure"], "min_days": 2, "max_days": 3},

    "Kausani": {"interests": ["Nature"], "min_days": 2, "max_days": 3},

    "Chandigarh": {"interests": ["Shopping", "Nature"], "min_days": 1, "max_days": 2},

    "Diu": {"interests": ["Beaches", "Historical Places"], "min_days": 2, "max_days": 3}
}

updated = 0
for name, data in interest_map.items():
    result = db.destinations.update_one(
        {"name": name},
        {"$set": {"interests": data["interests"], "min_days": data["min_days"], "max_days": data["max_days"]}}
    )
    if result.modified_count > 0:
        updated += 1

print(f"Updated {updated} destinations with interest tags and duration data")

missing = db.destinations.count_documents({"interests": {"$exists": False}})
print(f"Destinations still missing tags: {missing}")
