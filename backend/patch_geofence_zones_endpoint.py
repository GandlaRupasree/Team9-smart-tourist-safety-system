with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def get_geofence_zones():"
end_marker = '@app.route("/api/geofence-nearest"'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """def get_geofence_zones():
    destination_name = request.args.get("destination")
    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    location = dest.get("location", {})
    radius = dest.get("safe_zone_radius_km", 5)

    zones = []
    zones.append({
        "type": "safe",
        "label": f"{destination_name} Safe Zone",
        "lat": location.get("lat"),
        "lng": location.get("lng"),
        "radius_km": radius,
        "details": {"crime_rate": "Not available", "note": "Real-time crime data is not publicly available; this circle marks the destination's designated safe-travel radius only."}
    })
    for w in dest.get("warning_zones", []):
        if w.get("lat") is None or w.get("lng") is None:
            continue
        zones.append({
            "type": "warning",
            "label": w["name"],
            "lat": w["lat"],
            "lng": w["lng"],
            "radius_km": 2,
            "details": {"reason": "Forest or protected natural area (from OpenStreetMap)", "advice": "Stay on marked paths, be aware of wildlife, avoid travel after dark."}
        })
    for d in dest.get("danger_zones", []):
        if d.get("lat") is None or d.get("lng") is None:
            continue
        zones.append({
            "type": "danger",
            "label": d["name"],
            "lat": d["lat"],
            "lng": d["lng"],
            "radius_km": 2,
            "details": {"reason": "Military facility (from OpenStreetMap)", "advice": "Entry prohibited. Avoid this area completely."}
        })

    return jsonify({
        "destination": destination_name,
        "location": location,
        "safe_zone_radius_km": radius,
        "zones": zones,
        "emergency_contacts": dest.get("emergency_contacts", {
            "police": "100", "ambulance": "108", "fire": "101", "tourist_helpline": "1363"
        })
    })


"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched get_geofence_zones with real zones")
