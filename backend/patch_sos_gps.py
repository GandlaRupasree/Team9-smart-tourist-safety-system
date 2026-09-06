with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def trigger_sos():"
end_marker = '''return jsonify({
        "alert": alert,
        "emergency_contacts": contacts
    })'''

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx) + len(end_marker)

new_function = """def trigger_sos():
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
    })"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched trigger_sos with real lat/lng")
