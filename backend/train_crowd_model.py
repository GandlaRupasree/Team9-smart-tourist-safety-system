from dotenv import load_dotenv
import os
import random
import shutil
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
import joblib

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

random.seed(42)
np.random.seed(42)

if os.path.exists("crowd_model.pkl"):
    shutil.copy("crowd_model.pkl", "crowd_model_backup.pkl")
    print("Backed up old model to crowd_model_backup.pkl")

destinations = list(db.destinations.find({}))
print(f"Training on {len(destinations)} destinations")


def hour_factor(hour):
    peak = 13.5
    return max(0.3, 1 - ((hour - peak) ** 2) / 90)


rows = []
for dest in destinations:
    rating = dest.get("ratings", {}).get("avg", 4.0)
    review_count = dest.get("ratings", {}).get("count", 500)
    entry_fee = dest.get("entry_fee", 0)
    best_months = dest.get("season", {}).get("best_months", list(range(1, 13)))

    popularity = (review_count / 3000) * 0.7 + (rating / 5) * 0.3
    popularity = min(1.5, max(0.2, popularity))

    for _ in range(120):
        hour = random.randint(6, 20)
        day_of_week = random.randint(0, 6)
        month = random.randint(1, 12)
        is_weekend = 1 if day_of_week >= 5 else 0
        is_holiday = 1 if random.random() < 0.08 else 0
        is_festival = 1 if random.random() < 0.05 else 0
        in_season = 1 if month in best_months else 0

        val = 250 * popularity * hour_factor(hour)
        if is_weekend:
            val *= 1.45
        if is_holiday:
            val *= 1.25
        if is_festival:
            val *= 1.9
        val *= 1.3 if in_season else 0.7
        val *= max(0.7, 1 - entry_fee / 3000)
        val *= np.random.uniform(0.85, 1.15)
        val = max(20, val)

        rows.append({
            "hour": hour, "day_of_week": day_of_week, "month": month,
            "is_weekend": is_weekend, "is_holiday": is_holiday, "is_festival": is_festival,
            "in_season": in_season, "rating": rating, "review_count": review_count,
            "entry_fee": entry_fee, "visitors": val,
        })

df = pd.DataFrame(rows)
X = df.drop(columns=["visitors"])
y = df["visitors"]

model = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
model.fit(X, y)
joblib.dump(model, "crowd_model.pkl")

print(f"Trained on {len(df)} samples, saved new crowd_model.pkl")
importances = sorted(zip(X.columns, model.feature_importances_), key=lambda x: -x[1])
print("\nNew feature importance:")
for name, score in importances:
    bar = "#" * int(score * 50)
    print(f"  {name:15s} {score:.3f}  {bar}")
