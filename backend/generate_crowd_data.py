from dotenv import load_dotenv
import os
from pymongo import MongoClient
import random
from datetime import datetime, timedelta

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

db.crowd_logs.delete_many({})

destinations = list(db.destinations.find())
logs = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

festival_dates = set()
for dest in destinations:
    for event in dest.get("events", []):
        try:
            start = datetime.strptime(event["start_date"], "%Y-%m-%d")
            end = datetime.strptime(event["end_date"], "%Y-%m-%d")
            current = start
            while current <= end:
                festival_dates.add(current.date())
                current += timedelta(days=1)
        except:
            pass

current_date = start_date
while current_date <= end_date:
    is_weekend = current_date.weekday() >= 5
    is_holiday = current_date.day in [1, 15, 26] and current_date.month in [1, 8, 10]
    is_festival = current_date.date() in festival_dates
    month = current_date.month

    for dest in destinations:
        base_visitors = dest["ratings"]["avg"] * 100
        in_season = month in dest["season"]["best_months"]

        visitor_count = base_visitors
        if in_season:
            visitor_count *= random.uniform(1.4, 1.8)
        if is_weekend:
            visitor_count *= random.uniform(1.3, 1.6)
        if is_holiday:
            visitor_count *= random.uniform(1.5, 2.0)
        if is_festival:
            visitor_count *= random.uniform(1.8, 2.5)

        visitor_count *= random.uniform(0.85, 1.15)
        visitor_count = max(10, int(visitor_count))

        for hour in [9, 12, 15, 18]:
            hourly_factor = {9: 0.7, 12: 1.2, 15: 1.0, 18: 0.6}[hour]
            hourly_count = int(visitor_count * hourly_factor * random.uniform(0.9, 1.1))

            logs.append({
                "destination_id": str(dest["_id"]),
                "destination_name": dest["name"],
                "date": current_date.strftime("%Y-%m-%d"),
                "hour": hour,
                "day_of_week": current_date.weekday(),
                "month": month,
                "is_weekend": is_weekend,
                "is_holiday": is_holiday,
                "is_festival": is_festival,
                "in_season": in_season,
                "rating": dest["ratings"]["avg"],
                "review_count": dest["ratings"]["count"],
                "entry_fee": dest["entry_fee"],
                "visitor_count": hourly_count
            })

    current_date += timedelta(days=7)

result = db.crowd_logs.insert_many(logs)
print(f"Inserted {len(result.inserted_ids)} crowd log records")

