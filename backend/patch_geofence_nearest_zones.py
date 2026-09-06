with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '"zones": nearest.get("zones", []),'
new = '''"zones": (
            [{
                "type": "safe",
                "label": f"{nearest[\\'name\\']} Safe Zone",
                "lat": nearest["location"]["lat"],
                "lng": nearest["location"]["lng"],
                "radius_km": radius,
                "details": {"crime_rate": "Not available", "note": "Real-time crime data is not publicly available; this circle marks the destination's designated safe-travel radius only."}
            }] +
            [{
                "type": "warning",
                "label": w["name"],
                "lat": w["lat"],
                "lng": w["lng"],
                "radius_km": 2,
                "details": {"reason": "Forest or protected natural area (from OpenStreetMap)", "advice": "Stay on marked paths, be aware of wildlife, avoid travel after dark."}
            } for w in nearest.get("warning_zones", []) if w.get("lat") is not None and w.get("lng") is not None] +
            [{
                "type": "danger",
                "label": d["name"],
                "lat": d["lat"],
                "lng": d["lng"],
                "radius_km": 2,
                "details": {"reason": "Military facility (from OpenStreetMap)", "advice": "Entry prohibited. Avoid this area completely."}
            } for d in nearest.get("danger_zones", []) if d.get("lat") is not None and d.get("lng") is not None]
        ),'''

if old in content:
    content = content.replace(old, new)
    print("OK: geofence_nearest now builds real zones")
else:
    print("WARNING: anchor not found")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
