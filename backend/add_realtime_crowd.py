with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found, no change made")
    return content

# 1. Add requests import (if missing) + a live weather helper, right before the model load
old1 = """crowd_model = joblib.load("crowd_model.pkl")"""
new1 = """import requests as _requests_lib

crowd_model = joblib.load("crowd_model.pkl")


def get_weather_adjustment(lat, lng, date_str):
    """"""Live weather forecast -> a multiplier on predicted crowd size.
    Open-Meteo is free, no API key. Forecasts only exist ~16 days ahead;
    outside that window this safely returns a neutral 1.0 multiplier.""""""
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
        return 1.0, None"""
content = try_replace(content, old1, new1, "weather helper function")

# 2. Replace the crowd-prediction route: safe field access + live weather adjustment
old2 = """@app.route("/api/crowd-prediction")
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
    in_season = 1 if month in dest["season"]["best_months"] else 0

    features = pd.DataFrame([{
        "hour": hour,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "is_festival": is_festival,
        "in_season": in_season,
        "rating": dest["ratings"]["avg"],
        "entry_fee": dest["entry_fee"]
    }])

    predicted_count = crowd_model.predict(features)[0]

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
        "in_season": bool(in_season)
    })"""
new2 = """@app.route("/api/crowd-prediction")
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
    entry_fee = dest.get("entry_fee", 0)

    features = pd.DataFrame([{
        "hour": hour,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "is_festival": is_festival,
        "in_season": in_season,
        "rating": rating,
        "entry_fee": entry_fee
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
    })"""
content = try_replace(content, old2, new2, "crowd-prediction route")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
