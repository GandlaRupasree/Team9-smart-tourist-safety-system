with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def get_crowd_prediction():"
end_marker = "if __name__"

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """def get_crowd_prediction():
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
    })


"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched get_crowd_prediction successfully")
