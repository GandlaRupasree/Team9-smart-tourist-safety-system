with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

anchor = '@app.route("/api/geofence-check", methods=["POST"])'

new_route = '''@app.route("/api/geofence-nearest", methods=["POST"])
def geofence_nearest():
    data = request.get_json()
    user_lat = data.get("lat")
    user_lng = data.get("lng")

    if user_lat is None or user_lng is None:
        return jsonify({"error": "lat and lng are required"}), 400

    all_dests = list(db.destinations.find({"location": {"$exists": True}}))
    nearest = None
    nearest_distance = None

    for d in all_dests:
        loc = d.get("location")
        if not loc or "lat" not in loc or "lng" not in loc:
            continue
        dist = haversine_distance(float(user_lat), float(user_lng), loc["lat"], loc["lng"])
        if nearest is None or dist < nearest_distance:
            nearest = d
            nearest_distance = dist

    if nearest is None:
        return jsonify({"error": "no destinations with location data found"}), 404

    radius = nearest.get("safe_zone_radius_km", 5)
    is_inside = nearest_distance <= radius

    result = {
        "destination": nearest["name"],
        "safe_zone_radius_km": radius,
        "distance_from_center_km": round(nearest_distance, 2),
        "inside_safe_zone": is_inside,
        "status": "Safe" if is_inside else "Outside Safe Zone",
        "dest_lat": nearest["location"]["lat"],
        "dest_lng": nearest["location"]["lng"],
        "user_lat": float(user_lat),
        "user_lng": float(user_lng),
        "zones": nearest.get("zones", []),
        "emergency_contacts": nearest.get("emergency_contacts", {
            "police": "100", "ambulance": "108", "fire": "101", "tourist_helpline": "1363"
        })
    }

    if not is_inside:
        alert_id = "GEO" + "".join(random.choices(string.digits, k=6))
        db.geofence_alerts.insert_one({
            "alert_id": alert_id,
            "destination": nearest["name"],
            "distance_from_center_km": round(nearest_distance, 2),
            "radius_km": radius,
            "triggered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        result["alert_id"] = alert_id

    return jsonify(result)


'''

if anchor in content:
    content = content.replace(anchor, new_route + anchor, 1)
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: /api/geofence-nearest route added")
else:
    print("WARNING: anchor not found")
