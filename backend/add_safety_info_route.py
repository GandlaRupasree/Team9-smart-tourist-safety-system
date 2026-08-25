with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

anchor = "@app.route(\"/api/sos\", methods=[\"POST\"])"
insert_idx = content.index(anchor)

new_route = """@app.route("/api/safety-info")
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


"""

content = content[:insert_idx] + new_route + content[insert_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Added /api/safety-info route successfully")
