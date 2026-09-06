with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """    result = {
        "destination": destination_name,
        "safe_zone_radius_km": radius,
        "distance_from_center_km": round(distance_from_center, 2),
        "inside_safe_zone": is_inside,
        "status": "Safe" if is_inside else "Outside Safe Zone"
    }"""

new = """    result = {
        "destination": destination_name,
        "safe_zone_radius_km": radius,
        "distance_from_center_km": round(distance_from_center, 2),
        "inside_safe_zone": is_inside,
        "status": "Safe" if is_inside else "Outside Safe Zone",
        "dest_lat": dest_lat,
        "dest_lng": dest_lng,
        "user_lat": float(user_lat),
        "user_lng": float(user_lng)
    }"""

if old in content:
    content = content.replace(old, new, 1)
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: backend patched with coordinates")
else:
    print("WARNING: anchor not found")
