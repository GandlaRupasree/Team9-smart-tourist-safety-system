from dotenv import load_dotenv
import os
from pymongo import MongoClient
import random

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

existing_names = set(d["name"] for d in db.destinations.find({}, {"name": 1}))

category_interests = {
    "hill": ["Nature"],
    "beach": ["Beaches"],
    "heritage": ["Historical Places"],
    "wildlife": ["Wildlife", "Nature"],
    "religious": ["Religious Tourism"],
    "nature": ["Nature"],
    "adventure": ["Adventure", "Nature"],
    "city": ["Shopping", "Historical Places"]
}

category_attractions = {
    "hill": ["Viewpoint", "Local Trekking Trails", "Hill Station Market"],
    "beach": ["Main Beach", "Sunset Point", "Local Seafood Market"],
    "heritage": ["Historic Fort/Monument", "Old Town Market", "Local Museum"],
    "wildlife": ["National Park", "Safari Zone", "Nature Trail"],
    "religious": ["Main Temple", "Pilgrim Ghats", "Local Shrine Complex"],
    "nature": ["Scenic Point", "Local Waterfall", "Nature Walk"],
    "adventure": ["Adventure Sports Zone", "Trekking Base", "Camping Grounds"],
    "city": ["City Center", "Local Bazaar", "Heritage Quarter"]
}

season_defaults = {
    "hill": [3,4,5,9,10,11], "beach": [10,11,12,1,2,3], "heritage": [10,11,12,1,2,3],
    "wildlife": [10,11,12,1,2,3], "religious": [10,11,12,1,2,3], "nature": [9,10,11,3,4],
    "adventure": [9,10,11,3,4], "city": [10,11,12,1,2]
}

new_places = [
    ("Coimbatore", 11.0168, 76.9558, "city"), ("Yercaud", 11.7753, 78.2098, "hill"),
    ("Thekkady", 9.5916, 77.1600, "wildlife"), ("Kovalam", 8.4004, 76.9787, "beach"),
    ("Varkala", 8.7379, 76.7163, "beach"), ("Kanyakumari", 8.0883, 77.5385, "heritage"),
    ("Rameswaram", 9.2876, 79.3129, "religious"), ("Thanjavur", 10.7870, 79.1378, "heritage"),
    ("Mangalore", 12.9141, 74.8560, "beach"), ("Udupi", 13.3409, 74.7421, "religious"),
    ("Badami", 15.9149, 75.6766, "heritage"), ("Bijapur", 16.8302, 75.7100, "heritage"),
    ("Belur", 13.1629, 75.8648, "heritage"), ("Halebidu", 13.2135, 75.9990, "heritage"),
    ("Kabini", 11.9490, 76.3270, "wildlife"), ("Nagarhole", 12.0000, 76.1333, "wildlife"),
    ("Agumbe", 13.5083, 75.0928, "nature"), ("Murudeshwar", 14.0942, 74.4839, "religious"),
    ("Alibaug", 18.6414, 72.8722, "beach"), ("Matheran", 18.9871, 73.2650, "hill"),
    ("Kolhapur", 16.7050, 74.2433, "heritage"), ("Nashik", 19.9975, 73.7898, "religious"),
    ("Aurangabad", 19.8762, 75.3433, "heritage"), ("Shirdi", 19.7645, 74.4763, "religious"),
    ("Pandharpur", 17.6792, 75.3320, "religious"), ("Tadoba", 20.2333, 79.3333, "wildlife"),
    ("Pench", 21.6667, 79.3000, "wildlife"), ("Panchgani", 17.9247, 73.8077, "hill"),
    ("Karjat", 18.9107, 73.3236, "adventure"), ("Igatpuri", 19.6969, 73.5626, "nature"),
    ("Daman", 20.3974, 72.8328, "beach"), ("Silvassa", 20.2766, 73.0169, "nature"),
    ("Vadodara", 22.3072, 73.1812, "heritage"), ("Ahmedabad", 23.0225, 72.5714, "heritage"),
    ("Dwarka", 22.2442, 68.9685, "religious"), ("Palitana", 21.5222, 71.8266, "religious"),
    ("Junagadh", 21.5222, 70.4579, "heritage"), ("Sasan Gir", 21.1266, 70.7930, "wildlife"),
    ("Mount Abu", 24.5926, 72.7156, "hill"), ("Bikaner", 28.0229, 73.3119, "heritage"),
    ("Pushkar", 26.4899, 74.5511, "religious"), ("Chittorgarh", 24.8887, 74.6269, "heritage"),
    ("Bundi", 25.4305, 75.6499, "heritage"), ("Alwar", 27.5530, 76.6346, "heritage"),
    ("Sariska", 27.3300, 76.4000, "wildlife"), ("Kumbhalgarh", 25.1487, 73.5878, "heritage"),
    ("Neemrana", 27.9833, 76.3833, "heritage"), ("Deeg", 27.4667, 77.3333, "heritage"),
    ("Mathura", 27.4924, 77.6737, "religious"), ("Vrindavan", 27.5820, 77.7005, "religious"),
    ("Ayodhya", 26.7922, 82.1998, "religious"), ("Lucknow", 26.8467, 80.9462, "heritage"),
    ("Kanpur", 26.4499, 80.3319, "city"), ("Prayagraj", 25.4358, 81.8463, "religious"),
    ("Sarnath", 25.3811, 83.0231, "religious"), ("Chitrakoot", 25.2000, 80.8667, "religious"),
    ("Jhansi", 25.4484, 78.5685, "heritage"), ("Orchha", 25.3516, 78.6413, "heritage"),
    ("Gwalior", 26.2183, 78.1828, "heritage"), ("Sanchi", 23.4833, 77.7386, "heritage"),
    ("Pachmarhi", 22.4676, 78.4336, "hill"), ("Kanha", 22.3344, 80.6119, "wildlife"),
    ("Bandhavgarh", 23.7000, 81.0000, "wildlife"), ("Indore", 22.7196, 75.8577, "city"),
    ("Ujjain", 23.1765, 75.7885, "religious"), ("Omkareshwar", 22.2422, 76.1517, "religious"),
    ("Maheshwar", 22.1786, 75.5883, "heritage"), ("Chitrakote Falls", 19.1897, 81.6650, "nature"),
    ("Raipur", 21.2514, 81.6296, "city"), ("Jagdalpur", 19.0748, 82.0338, "nature"),
    ("Ranchi", 23.3441, 85.3096, "nature"), ("Netarhat", 23.4700, 84.2600, "hill"),
    ("Betla", 23.8833, 84.1833, "wildlife"), ("Patna", 25.5941, 85.1376, "heritage"),
    ("Nalanda", 25.1358, 85.4436, "heritage"), ("Rajgir", 25.0280, 85.4210, "religious"),
    ("Vaishali", 25.9866, 85.1281, "religious"), ("Digha", 21.6270, 87.5088, "beach"),
    ("Mandarmani", 21.6667, 87.7333, "beach"), ("Bishnupur", 23.0742, 87.3200, "heritage"),
    ("Shantiniketan", 23.6800, 87.6800, "heritage"), ("Murshidabad", 24.1833, 88.2667, "heritage"),
    ("Cherrapunji", 25.2702, 91.7323, "nature"), ("Mawlynnong", 25.2010, 91.9186, "nature"),
    ("Tawang", 27.5859, 91.8594, "religious"), ("Ziro Valley", 27.6000, 93.8300, "nature"),
    ("Kohima", 25.6751, 94.1086, "heritage"), ("Imphal", 24.8170, 93.9368, "heritage"),
    ("Loktak Lake", 24.5500, 93.7833, "nature"), ("Aizawl", 23.7271, 92.7176, "nature"),
    ("Agartala", 23.8315, 91.2868, "heritage"), ("Majuli", 26.9500, 94.1667, "nature"),
    ("Guwahati", 26.1445, 91.7362, "religious"), ("Tezpur", 26.6338, 92.8000, "nature"),
    ("Manas National Park", 26.6667, 91.0000, "wildlife"), ("Dibrugarh", 27.4728, 94.9120, "nature"),
    ("Coonoor", 11.3530, 76.7959, "hill"), ("Yelagiri", 12.5833, 78.6333, "hill"),
    ("Hogenakkal", 12.1167, 77.7667, "nature"), ("Chettinad", 10.2000, 78.7833, "heritage"),
    ("Mahabalipuram", 12.6208, 80.1926, "heritage"), ("Chennai", 13.0827, 80.2707, "city"),
    ("Vellore", 12.9165, 79.1325, "religious"), ("Tiruchirappalli", 10.7905, 78.7047, "religious"),
    ("Velankanni", 10.6800, 79.8500, "religious"), ("Kumarakom", 9.6167, 76.4167, "nature"),
    ("Thrissur", 10.5276, 76.2144, "religious"), ("Kozhikode", 11.2588, 75.7804, "heritage"),
    ("Kannur", 11.8745, 75.3704, "beach"), ("Bekal", 12.3833, 75.0333, "beach"),
    ("Vagamon", 9.6883, 76.9033, "hill"), ("Ponmudi", 8.7500, 77.1167, "hill"),
    ("Silent Valley", 11.0833, 76.4167, "wildlife"), ("Visakhapatnam", 17.6868, 83.2185, "beach"),
    ("Vijayawada", 16.5062, 80.6480, "religious"), ("Amaravati", 16.5730, 80.3576, "heritage"),
    ("Srisailam", 16.0739, 78.8697, "religious"), ("Warangal", 17.9689, 79.5941, "heritage"),
    ("Nagarjuna Sagar", 16.5667, 79.3167, "heritage"), ("Bhadrachalam", 17.6688, 80.8933, "religious"),
    ("Lepakshi", 13.8000, 77.6000, "heritage"), ("Horsley Hills", 13.6500, 78.4000, "hill"),
    ("Gandikota", 14.8228, 78.2814, "nature"), ("Bhubaneswar", 20.2961, 85.8245, "heritage"),
    ("Chilika Lake", 19.7000, 85.3167, "nature"), ("Similipal", 21.6167, 86.3167, "wildlife"),
    ("Cuttack", 20.4625, 85.8828, "heritage"), ("Gopalpur", 19.2667, 84.9167, "beach")
]

destinations_to_insert = []
for name, lat, lng, category in new_places:
    if name in existing_names:
        continue
    interests = category_interests[category]
    attractions = [a.replace("[Name]", name) if "[Name]" in a else f"{name} {a}" if category in ["hill","nature"] else a for a in category_attractions[category]]
    season = season_defaults[category]
    entry_fee = random.choice([0, 0, 20, 30, 50, 100]) if category != "heritage" else random.choice([25, 40, 100, 300])
    avg_cost = random.randint(1500, 3200)
    rating = round(random.uniform(3.9, 4.7), 1)
    review_count = random.randint(200, 3000)

    destinations_to_insert.append({
        "name": name,
        "ratings": {"avg": rating, "count": review_count},
        "reviews": [],
        "attractions": attractions,
        "interests": interests,
        "min_days": 1,
        "max_days": 3 if category in ["heritage","religious","city"] else 4,
        "season": {"best_months": season},
        "weather": {"avg_temp": 24, "condition": "Pleasant"},
        "location": {"lat": lat, "lng": lng},
        "entry_fee": entry_fee,
        "events": [],
        "avg_cost": avg_cost,
        "safe_zone_radius_km": round(random.uniform(3, 8), 1),
        "emergency_contacts": {"police": "100", "ambulance": "108", "tourist_helpline": "1363", "fire": "101"}
    })

if destinations_to_insert:
    result = db.destinations.insert_many(destinations_to_insert)
    print(f"Inserted {len(result.inserted_ids)} new destinations")
else:
    print("No new destinations to insert (all already exist)")

print(f"Total destinations now: {db.destinations.count_documents({})}")
