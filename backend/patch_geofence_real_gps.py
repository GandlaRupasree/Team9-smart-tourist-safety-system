with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def geofence_check():"
end_marker = '@app.route("/api/sos"'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """def geofence_check():
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


"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched geofence_check to use real lat/lng")
