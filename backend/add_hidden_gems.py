from dotenv import load_dotenv
import os
from pymongo import MongoClient
import random

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

gem_templates = [
    "{} - a quiet local viewpoint away from the crowds",
    "The old {} lane, known mostly to locals",
    "A small family-run eatery near {} serving regional specialties",
    "{} backwater/lakeside spot, great for an early morning walk",
    "An unmarked trail near {} popular with local trekkers",
    "A centuries-old well/step-structure near {} rarely visited by tourists",
    "Local artisan workshops near {} where you can watch traditional crafts being made",
    "A small hilltop shrine near {} with panoramic views",
    "{} weekly local market - best visited early morning for authentic produce",
    "A hidden waterfall/stream near {}, a short walk from the main road"
]

destinations = list(db.destinations.find())
updated = 0
for dest in destinations:
    name = dest["name"]
    picks = random.sample(gem_templates, 3)
    hidden_gems = [g.format(name) for g in picks]
    db.destinations.update_one(
        {"_id": dest["_id"]},
        {"$set": {"hidden_gems": hidden_gems}}
    )
    updated += 1

print(f"Added hidden gems to {updated} destinations")
