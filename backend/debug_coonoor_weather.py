from dotenv import load_dotenv
import os
import requests
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

dest = db.destinations.find_one({"name": "Coonoor"})
if not dest:
    print("Coonoor not found in destinations collection at all!")
else:
    location = dest.get("location")
    print("Coonoor location field:", location)

    if location and location.get("lat") and location.get("lng"):
        print("\nCalling Open-Meteo directly with these coordinates...")
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["lat"],
                "longitude": location["lng"],
                "daily": "precipitation_probability_max,weathercode",
                "timezone": "Asia/Kolkata",
                "start_date": "2026-08-29",
                "end_date": "2026-08-29",
            },
            timeout=8,
        )
        print("Status code:", resp.status_code)
        print("Response:", resp.json())
    else:
        print("\nNo usable lat/lng - this is why weather came back empty.")
