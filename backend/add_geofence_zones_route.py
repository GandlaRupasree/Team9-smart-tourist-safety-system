with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

anchor = '@app.route("/api/geofence-check", methods=["POST"])'

new_route = """@app.route("/api/geofence-zones")
def get_geofence_zones():
    destination_name = request.args.get("destination")
    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    return jsonify({
        "destination": destination_name,
        "location": dest.get("location", {}),
        "safe_zone_radius_km": dest.get("safe_zone_radius_km", 5),
        "zones": dest.get("zones", []),
        "emergency_contacts": dest.get("emergency_contacts", {
            "police": "100", "ambulance": "108", "fire": "101", "tourist_helpline": "1363"
        })
    })


"""

if anchor in content:
    content = content.replace(anchor, new_route + anchor, 1)
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: /api/geofence-zones route added")
else:
    print("WARNING: anchor not found")
