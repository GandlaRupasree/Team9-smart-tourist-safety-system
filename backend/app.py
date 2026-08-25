from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import math
import joblib
import pandas as pd
from datetime import datetime
import random
import string
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)
client = MongoClient(os.getenv("MONGO_URI"))
db = client["toursafe"]

import requests as _requests_lib

crowd_model = joblib.load("crowd_model.pkl")


def get_weather_adjustment(lat, lng, date_str):
    # Live weather forecast -> a multiplier on predicted crowd size.
    # Open-Meteo is free, no API key. Forecasts only exist ~16 days ahead;
    # outside that window this safely returns a neutral 1.0 multiplier.
    if lat is None or lng is None:
        return 1.0, None

    try:
        resp = _requests_lib.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lng,
                "daily": "precipitation_probability_max,weathercode",
                "timezone": "Asia/Kolkata",
                "start_date": date_str,
                "end_date": date_str,
            },
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        daily = data.get("daily", {})
        rain_prob = daily.get("precipitation_probability_max", [None])[0]
        code = daily.get("weathercode", [None])[0]

        if rain_prob is None:
            return 1.0, None

        if rain_prob >= 70:
            return 0.65, {"rain_probability": rain_prob, "condition": "Heavy rain likely"}
        elif rain_prob >= 40:
            return 0.85, {"rain_probability": rain_prob, "condition": "Rain possible"}
        elif code in (0, 1):
            return 1.05, {"rain_probability": rain_prob, "condition": "Clear skies"}
        else:
            return 1.0, {"rain_probability": rain_prob, "condition": "Normal conditions"}
    except Exception:
        return 1.0, None

def haversine_distance(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def is_in_season(best_months):
    current_month = datetime.now().month
    return current_month in best_months

def get_image_url(destination_name):
    seed = destination_name.replace(" ", "")
    return f"https://picsum.photos/seed/{seed}/400/300"

def calculate_sustainability_score(dest, distance_km):
    score = 50

    if distance_km < 200:
        score += 20
    elif distance_km < 500:
        score += 10
    elif distance_km > 1500:
        score -= 15

    interests = dest.get("interests", [])
    if "Wildlife" in interests or "Nature" in interests:
        score += 15

    if dest["entry_fee"] > 200:
        score += 10
    elif dest["entry_fee"] == 0:
        score -= 5

    if dest["ratings"]["count"] > 3000:
        score -= 10

    score = max(0, min(100, score))

    if score >= 75:
        label = "Highly Sustainable"
    elif score >= 50:
        label = "Moderately Sustainable"
    else:
        label = "Lower Sustainability"

    return {"score": score, "label": label}

TRANSPORT_COST_PER_KM = {"Bus": 1.5, "Train": 1.2, "Flight": 6.0, "Private Vehicle": 8.0}
ACCOMMODATION_MULTIPLIER = {"Hostel": 0.5, "Homestay": 0.7, "Hotel": 1.0, "Resort": 1.8}

@app.route("/")
def home():
    return "TourSafe backend is running"

def get_dest_image(dest):
    if dest.get("verified_image_url"):
        return dest["verified_image_url"]

    for photo in dest.get("attraction_photos", []):
        if photo.get("image_url"):
            return photo["image_url"]

    seed = dest["name"].replace(" ", "")
    return f"https://picsum.photos/seed/{seed}/400/300"

@app.route("/api/recommendations")
def get_recommendations():
    user_lat = float(request.args.get("lat", 12.9716))
    user_lng = float(request.args.get("lng", 77.5946))
    max_budget = request.args.get("max_budget", type=float)
    max_distance = request.args.get("max_distance", type=float)
    season_only = request.args.get("season_only", "false").lower() == "true"
    search = request.args.get("search", "").strip().lower()
    sort_by = request.args.get("sort_by", "score")

    destinations = list(db.destinations.find())
    results = []

    for dest in destinations:
        dist = haversine_distance(user_lat, user_lng, dest["location"]["lat"], dest["location"]["lng"])
        in_season = is_in_season(dest["season"]["best_months"])

        if max_budget is not None and dest["avg_cost"] > max_budget:
            continue
        if max_distance is not None and dist > max_distance:
            continue
        if season_only and not in_season:
            continue

        if search:
            name_match = search in dest["name"].lower()
            attraction_match = any(search in a.lower() for a in dest["attractions"])
            if not (name_match or attraction_match):
                continue

        score = dest["ratings"]["avg"] * 2
        score -= dist * 0.01
        score += 5 if in_season else 0
        score -= dest["entry_fee"] * 0.001

        sustainability = calculate_sustainability_score(dest, dist)

        results.append({
            "name": dest["name"],
            "rating": dest["ratings"]["avg"],
            "attractions": dest["attractions"],
            "distance_km": round(dist, 1),
            "entry_fee": dest["entry_fee"],
            "avg_cost": dest["avg_cost"],
            "in_season": in_season,
            "score": round(score, 2),
            "image_url": get_dest_image(dest),
            "sustainability_score": sustainability["score"],
            "sustainability_label": sustainability["label"]
        })

    sort_key_map = {
        "score": lambda x: x["score"],
        "rating": lambda x: x["rating"],
        "cost_low": lambda x: -x["avg_cost"],
        "distance": lambda x: -x["distance_km"]
    }
    key_func = sort_key_map.get(sort_by, sort_key_map["score"])
    results.sort(key=key_func, reverse=True)

    return jsonify(results)

@app.route("/api/smart-recommendations", methods=["POST"])
def smart_recommendations():
    data = request.get_json()

    user_lat = float(data.get("lat", 12.9716))
    user_lng = float(data.get("lng", 77.5946))
    budget = float(data.get("budget", 20000))
    duration_days = int(data.get("duration_days", 3))
    interests = data.get("interests", [])
    num_travelers = int(data.get("num_travelers", 1))
    age_group = data.get("age_group", "Adult")
    transport = data.get("transport", "Train")
    accommodation = data.get("accommodation", "Hotel")

    destinations = list(db.destinations.find())
    results = []

    for dest in destinations:
        dist = haversine_distance(user_lat, user_lng, dest["location"]["lat"], dest["location"]["lng"])
        in_season = is_in_season(dest["season"]["best_months"])

        dest_interests = dest.get("interests", [])
        min_days = dest.get("min_days", 1)
        max_days = dest.get("max_days", 10)

        transport_cost_per_person = dist * 2 * TRANSPORT_COST_PER_KM.get(transport, 1.5)
        accommodation_cost_per_night = dest["avg_cost"] * ACCOMMODATION_MULTIPLIER.get(accommodation, 1.0)
        total_cost_per_person = transport_cost_per_person + (accommodation_cost_per_night * duration_days)
        total_trip_cost = total_cost_per_person * num_travelers

        if total_trip_cost > budget:
            continue
        if duration_days < min_days or duration_days > max_days:
            continue

        interest_match_count = len(set(interests) & set(dest_interests)) if interests else 0
        if interests and interest_match_count == 0:
            continue

        score = dest["ratings"]["avg"] * 2
        score += interest_match_count * 3
        score += 5 if in_season else 0
        score -= dist * 0.005
        score -= (total_trip_cost / budget) * 5

        if score < 0:
            continue

        sustainability = calculate_sustainability_score(dest, dist)

        results.append({
            "name": dest["name"],
            "rating": dest["ratings"]["avg"],
            "attractions": dest["attractions"],
            "interests": dest_interests,
            "distance_km": round(dist, 1),
            "estimated_total_cost": round(total_trip_cost),
            "cost_per_person": round(total_cost_per_person),
            "in_season": in_season,
            "recommended_days": f"{min_days}-{max_days} days",
            "score": round(score, 2),
            "image_url": get_dest_image(dest),
            "sustainability_score": sustainability["score"],
            "sustainability_label": sustainability["label"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results)

@app.route("/api/itinerary")
def get_itinerary():
    destination_name = request.args.get("destination")
    duration_days = int(request.args.get("duration_days", 3))

    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    attractions = [a["name"] for a in dest.get("real_attractions", [])] or list(dest.get("attractions", []))
    hidden_gems = [f"(Local Tip) {g}" for g in dest.get("hidden_gems", [])]
    name = dest["name"]

    real_spots = attractions + hidden_gems
    has_real_spots = len(real_spots) > 0

    idx_pointer = [0]
    seen_once = set()

    def next_spot():
        if not has_real_spots:
            return "Explore the local area (no verified attractions listed for this destination yet)"
        spot = real_spots[idx_pointer[0] % len(real_spots)]
        is_repeat = spot in seen_once
        seen_once.add(spot)
        idx_pointer[0] += 1
        return f"Revisit - {spot}" if is_repeat else spot

    plan = []
    for day_num in range(1, duration_days + 1):
        if day_num == 1:
            title = f"Arrival in {name}"
        elif day_num == duration_days and duration_days > 1:
            title = f"Departure from {name}"
        else:
            title = f"Exploring {name}"

        if day_num == 1:
            morning = [
                "9:00 AM - Breakfast",
                "10:00 AM - Arrive and check into accommodation",
                f"11:00 AM - {next_spot()}",
                "1:00 PM - Lunch"
            ]
            afternoon = [
                f"2:30 PM - {next_spot()}",
                "4:00 PM - Free time / local exploration"
            ]
            night = [
                f"6:00 PM - {next_spot()}",
                "7:30 PM - Try local cuisine for dinner",
                "9:00 PM - Relax at your accommodation"
            ]
        elif day_num == duration_days and duration_days > 1:
            morning = [
                "7:30 AM - Breakfast",
                f"8:30 AM - {next_spot()}",
                "10:30 AM - Free time / optional shopping"
            ]
            afternoon = [
                "12:30 PM - Lunch",
                "2:00 PM - Check out of accommodation",
                "3:00 PM - Head back / departure prep"
            ]
            night = [
                "Evening - Begin your return journey"
            ]
        else:
            morning = [
                "7:30 AM - Breakfast",
                f"8:30 AM - {next_spot()}",
                "12:30 PM - Lunch"
            ]
            afternoon = [
                f"2:00 PM - {next_spot()}",
                "4:30 PM - Free time / local exploration"
            ]
            night = [
                f"6:00 PM - {next_spot()}",
                "7:30 PM - Dinner",
                "9:00 PM - Relax / optional evening activity"
            ]

        plan.append({
            "day": day_num,
            "title": title,
            "morning": morning,
            "afternoon": afternoon,
            "night": night
        })

    return jsonify({
        "destination": dest["name"],
        "duration_days": duration_days,
        "itinerary": plan,
        "verified_attraction_count": len(real_spots)
    })


@app.route("/api/real-hotels")
def get_real_hotels():
    destination_name = request.args.get("destination")
    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    real = list(db.real_hotels.find({"destination_name": destination_name, "hotel_name": {"$ne": None}}))
    for h in real:
        h["_id"] = str(h["_id"])

    return jsonify({
        "has_real_data": len(real) > 0,
        "hotels": real
    })

@app.route("/api/accommodations")
def get_accommodations():
    destination_name = request.args.get("destination")
    acc_type = request.args.get("type")

    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    query = {"destination_name": destination_name}
    if acc_type:
        query["type"] = acc_type

    listings = list(db.accommodations.find(query))
    for listing in listings:
        listing["_id"] = str(listing["_id"])

    listings.sort(key=lambda x: -x["rating"])
    return jsonify(listings)

@app.route("/api/book", methods=["POST"])
def book_accommodation():
    data = request.get_json()
    accommodation_id = data.get("accommodation_id")
    source = data.get("source", "synthetic")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    adults = int(data.get("adults", 1))
    children = int(data.get("children", 0))
    device_id = data.get("device_id")

    if not accommodation_id:
        return jsonify({"error": "accommodation_id is required"}), 400
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400
    if not check_in or not check_out:
        return jsonify({"error": "check_in and check_out dates are required"}), 400
    if adults < 1:
        return jsonify({"error": "at least 1 adult is required"}), 400

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "check_in and check_out must be in YYYY-MM-DD format"}), 400

    nights = (check_out_date - check_in_date).days
    if nights < 1:
        return jsonify({"error": "check_out must be at least 1 day after check_in"}), 400

    guests = adults + children

    if source == "real":
        listing = db.real_hotels.find_one({"_id": ObjectId(accommodation_id)})
        if not listing:
            return jsonify({"error": "hotel not found"}), 404
        hotel_name = listing["hotel_name"]
        destination = listing["destination_name"]
        hotel_type = listing.get("tourism_type", "hotel")
        price_per_night = listing.get("estimated_price_per_night", 2000)
        address = listing.get("address", "")
    else:
        listing = db.accommodations.find_one({"_id": ObjectId(accommodation_id)})
        if not listing:
            return jsonify({"error": "accommodation not found"}), 404
        hotel_name = listing["name"]
        destination = listing["destination_name"]
        hotel_type = listing["type"]
        price_per_night = listing["price_per_night"]
        address = ""

    total_cost = price_per_night * nights
    booking_id = "TS" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    booking = {
        "booking_id": booking_id,
        "device_id": device_id,
        "accommodation_name": hotel_name,
        "destination": destination,
        "type": hotel_type,
        "address": address,
        "source": source,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "adults": adults,
        "children": children,
        "guests": guests,
        "price_per_night": price_per_night,
        "total_cost": total_cost,
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db.bookings.insert_one(booking)
    booking.pop("_id", None)
    return jsonify(booking)

@app.route("/api/bookings")
def get_bookings():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400
    bookings = list(db.bookings.find({"device_id": device_id}).sort("booked_at", -1))
    for b in bookings:
        b["_id"] = str(b["_id"])
    return jsonify(bookings)

@app.route("/api/incidents", methods=["POST"])
def report_incident():
    data = request.get_json()
    destination_name = data.get("destination")
    incident_type = data.get("incident_type", "Other")
    description = data.get("description", "")
    severity = data.get("severity", "Medium")

    if not destination_name:
        return jsonify({"error": "destination is required"}), 400

    report_id = "INC" + "".join(random.choices(string.digits, k=6))
    incident = {
        "report_id": report_id,
        "destination": destination_name,
        "incident_type": incident_type,
        "description": description,
        "severity": severity,
        "status": "Reported",
        "reported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.incidents.insert_one(incident)
    incident.pop("_id", None)

    return jsonify(incident)

@app.route("/api/incidents")
def get_incidents():
    destination_name = request.args.get("destination")
    query = {}
    if destination_name:
        query["destination"] = destination_name

    incidents = list(db.incidents.find(query).sort("reported_at", -1))
    for i in incidents:
        i["_id"] = str(i["_id"])

    return jsonify(incidents)

import requests as _requests

def get_wikipedia_image_for(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(chr(32), chr(95))}"
        resp = _requests.get(url, timeout=4, headers={"User-Agent": "TourSafeStudentProject/1.0"})
        if resp.status_code == 200:
            data = resp.json()
            if "thumbnail" in data and "source" in data["thumbnail"]:
                return data["thumbnail"]["source"]
    except Exception:
        pass
    return None

@app.route("/api/attractions")
def get_attractions():
    destination_name = request.args.get("destination")
    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    cached = dest.get("attraction_photos")
    if cached:
        return jsonify({"destination": destination_name, "attractions": cached})

    attractions = dest.get("attractions", [])
    results = []
    for attr in attractions:
        img = get_wikipedia_image_for(attr) or get_wikipedia_image_for(f"{attr} {destination_name}")
        results.append({"name": attr, "image_url": img})

    db.destinations.update_one({"_id": dest["_id"]}, {"$set": {"attraction_photos": results}})

    return jsonify({"destination": destination_name, "attractions": results})

@app.route("/api/geofence-check", methods=["POST"])
def geofence_check():
    data = request.get_json()
    destination_name = data.get("destination")
    user_lat = data.get("lat")
    user_lng = data.get("lng")

    if not destination_name:
        return jsonify({"error": "destination is required"}), 400
    if user_lat is None or user_lng is None:
        return jsonify({"error": "lat and lng are required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    dest_lat = dest["location"]["lat"]
    dest_lng = dest["location"]["lng"]
    radius = dest.get("safe_zone_radius_km", 5)

    distance_from_center = haversine_distance(float(user_lat), float(user_lng), dest_lat, dest_lng)
    is_inside = distance_from_center <= radius

    result = {
        "destination": destination_name,
        "safe_zone_radius_km": radius,
        "distance_from_center_km": round(distance_from_center, 2),
        "inside_safe_zone": is_inside,
        "status": "Safe" if is_inside else "Outside Safe Zone"
    }

    if not is_inside:
        alert_id = "GEO" + "".join(random.choices(string.digits, k=6))
        db.geofence_alerts.insert_one({
            "alert_id": alert_id,
            "destination": destination_name,
            "distance_from_center_km": round(distance_from_center, 2),
            "radius_km": radius,
            "triggered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        result["alert_id"] = alert_id

    return jsonify(result)


@app.route("/api/safety-info")
def get_safety_info():
    destination_name = request.args.get("destination")
    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    contacts = dest.get("emergency_contacts", {"police": "100", "ambulance": "108", "tourist_helpline": "1363", "fire": "101"})

    return jsonify({
        "destination": destination_name,
        "hospitals": dest.get("nearby_hospitals", []),
        "police_stations": dest.get("nearby_police", []),
        "emergency_contacts": contacts,
        "safe_zone_radius_km": dest.get("safe_zone_radius_km", 5)
    })


@app.route("/api/sos", methods=["POST"])
def trigger_sos():
    data = request.get_json()
    destination_name = data.get("destination")
    situation = data.get("situation", "General emergency")
    location_note = data.get("location_note", "")
    user_lat = data.get("lat")
    user_lng = data.get("lng")

    dest = db.destinations.find_one({"name": destination_name}) if destination_name else None
    contacts = dest.get("emergency_contacts", {"police": "100", "ambulance": "108", "tourist_helpline": "1363", "fire": "101"}) if dest else {"police": "100", "ambulance": "108", "tourist_helpline": "1363", "fire": "101"}

    alert_id = "SOS" + "".join(random.choices(string.digits, k=6))
    alert = {
        "alert_id": alert_id,
        "destination": destination_name,
        "situation": situation,
        "location_note": location_note,
        "lat": user_lat,
        "lng": user_lng,
        "status": "Alert Sent",
        "triggered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.sos_alerts.insert_one(alert)
    alert.pop("_id", None)

    return jsonify({
        "alert": alert,
        "emergency_contacts": contacts
    })

@app.route("/api/bookings/summary")
def bookings_summary():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400
    confirmed = list(db.bookings.find({"status": "Confirmed", "device_id": device_id}))
    total_spend = sum(b["total_cost"] for b in confirmed)
    total_nights = sum(b["nights"] for b in confirmed)
    destinations_visited = list(set(b["destination"] for b in confirmed))

    return jsonify({
        "total_bookings": len(confirmed),
        "total_spend": total_spend,
        "total_nights": total_nights,
        "destinations_count": len(destinations_visited),
        "destinations": destinations_visited
    })

@app.route("/api/bookings/cancel", methods=["POST"])
def cancel_booking():
    data = request.get_json()
    booking_id = data.get("booking_id")
    device_id = data.get("device_id")

    if not booking_id:
        return jsonify({"error": "booking_id is required"}), 400
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    booking = db.bookings.find_one({"booking_id": booking_id, "device_id": device_id})
    if not booking:
        return jsonify({"error": "booking not found"}), 404

    booked_at = datetime.strptime(booking["booked_at"], "%Y-%m-%d %H:%M:%S")
    hours_since_booking = (datetime.now() - booked_at).total_seconds() / 3600

    if hours_since_booking <= 24:
        refund_percent = 100
    else:
        refund_percent = 50

    refund_amount = round(booking["total_cost"] * refund_percent / 100)

    db.bookings.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": "Cancelled", "refund_percent": refund_percent, "refund_amount": refund_amount}}
    )

    return jsonify({
        "booking_id": booking_id,
        "status": "Cancelled",
        "refund_percent": refund_percent,
        "refund_amount": refund_amount
    })


@app.route("/api/crowd-prediction")
def get_crowd_prediction():
    destination_name = request.args.get("destination")
    hour = int(request.args.get("hour", 12))
    date_str = request.args.get("date")
    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400
    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404
    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        target_date = datetime.now()
    day_of_week = target_date.weekday()
    month = target_date.month
    is_weekend = 1 if day_of_week >= 5 else 0
    is_holiday = 1 if (target_date.day in [1, 15, 26] and month in [1, 8, 10]) else 0
    is_festival = 0
    for event in dest.get("events", []):
        try:
            start = datetime.strptime(event["start_date"], "%Y-%m-%d")
            end = datetime.strptime(event["end_date"], "%Y-%m-%d")
            if start <= target_date <= end:
                is_festival = 1
        except:
            pass

    best_months = dest.get("season", {}).get("best_months", [])
    in_season = 1 if month in best_months else 0
    rating = dest.get("ratings", {}).get("avg", 4.0)
    review_count = dest.get("ratings", {}).get("count", 0)
    entry_fee = dest.get("entry_fee", 0)
    lodging_count = db.real_hotels.count_documents({"destination_name": destination_name})

    features = pd.DataFrame([{
        "hour": hour,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "is_festival": is_festival,
        "in_season": in_season,
        "rating": rating,
        "review_count": review_count,
        "entry_fee": entry_fee,
        "lodging_count": lodging_count
    }])
    predicted_count = crowd_model.predict(features)[0]

    location = dest.get("location", {})
    weather_factor, weather_info = get_weather_adjustment(
        location.get("lat"), location.get("lng"), target_date.strftime("%Y-%m-%d")
    )
    predicted_count = predicted_count * weather_factor

    if predicted_count < 300:
        crowd_level = "Low"
    elif predicted_count < 700:
        crowd_level = "Medium"
    else:
        crowd_level = "High"
    return jsonify({
        "destination": destination_name,
        "date": target_date.strftime("%Y-%m-%d"),
        "hour": hour,
        "predicted_visitors": round(predicted_count),
        "crowd_level": crowd_level,
        "is_weekend": bool(is_weekend),
        "is_festival": bool(is_festival),
        "in_season": bool(in_season),
        "weather": weather_info
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


















