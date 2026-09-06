with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

anchor = '@app.route("/api/geofence-nearest", methods=["POST"])'
insert_idx = content.index(anchor)

new_route = '''import requests as _geo_requests_lib

GEOAPIFY_LIVE_KEY = os.getenv("GEOAPIFY_API_KEY")


def _fetch_live_places(lat, lon, category, radius, limit=5):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": category,
        "filter": f"circle:{lon},{lat},{radius}",
        "bias": f"proximity:{lon},{lat}",
        "limit": limit,
        "lang": "en",
        "apiKey": GEOAPIFY_LIVE_KEY,
    }
    try:
        r = _geo_requests_lib.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return []
    results = []
    for f in data.get("features", []):
        props = f.get("properties", {})
        name = props.get("name")
        if not name:
            continue
        results.append({"name": name, "lat": props.get("lat"), "lng": props.get("lon")})
    return results


@app.route("/api/geofence-live", methods=["POST"])
def geofence_live():
    data = request.get_json()
    user_lat = data.get("lat")
    user_lng = data.get("lng")

    if user_lat is None or user_lng is None:
        return jsonify({"error": "lat and lng are required"}), 400

    user_lat = float(user_lat)
    user_lng = float(user_lng)
    radius = 15000

    zones = []
    for name, lat_v, lng_v in (
        _fetch_live_places(user_lat, user_lng, "natural.forest", radius, 3) and
        [(f["name"], f["lat"], f["lng"]) for f in _fetch_live_places(user_lat, user_lng, "natural.forest", radius, 3)]
    ) or []:
        zones.append({
            "type": "warning", "label": name, "lat": lat_v, "lng": lng_v, "radius_km": 2,
            "details": {"reason": "Forest area (from OpenStreetMap, live lookup)", "advice": "Stay on marked paths, be aware of wildlife, avoid travel after dark."}
        })
    for f in _fetch_live_places(user_lat, user_lng, "natural.protected_area", radius, 3):
        zones.append({
            "type": "warning", "label": f["name"], "lat": f["lat"], "lng": f["lng"], "radius_km": 2,
            "details": {"reason": "Protected natural area (from OpenStreetMap, live lookup)", "advice": "Stay on marked paths, be aware of wildlife, avoid travel after dark."}
        })
    for f in _fetch_live_places(user_lat, user_lng, "building.military", radius, 2):
        zones.append({
            "type": "danger", "label": f["name"], "lat": f["lat"], "lng": f["lng"], "radius_km": 2,
            "details": {"reason": "Military facility (from OpenStreetMap, live lookup)", "advice": "Entry prohibited. Avoid this area completely."}
        })
    for f in _fetch_live_places(user_lat, user_lng, "natural.mountain.cliff", radius, 2):
        zones.append({
            "type": "danger", "label": f["name"], "lat": f["lat"], "lng": f["lng"], "radius_km": 1,
            "details": {"reason": "Cliff / steep terrain (from OpenStreetMap, live lookup)", "advice": "Fall risk. Stay away from the edge, especially in poor visibility or rain."}
        })
    for f in _fetch_live_places(user_lat, user_lng, "natural.water.whitewater", radius, 2):
        zones.append({
            "type": "danger", "label": f["name"], "lat": f["lat"], "lng": f["lng"], "radius_km": 1,
            "details": {"reason": "Rapids / fast-moving water (from OpenStreetMap, live lookup)", "advice": "Drowning risk. Avoid entering the water here without a guide."}
        })

    all_dests = list(db.destinations.find({"location": {"$exists": True}}))
    nearest = None
    nearest_distance = None
    for d in all_dests:
        loc = d.get("location")
        if not loc or "lat" not in loc or "lng" not in loc:
            continue
        dist = haversine_distance(user_lat, user_lng, loc["lat"], loc["lng"])
        if nearest is None or dist < nearest_distance:
            nearest = d
            nearest_distance = dist

    return jsonify({
        "user_lat": user_lat,
        "user_lng": user_lng,
        "zones": zones,
        "nearest_destination": nearest["name"] if nearest else None,
        "nearest_distance_km": round(nearest_distance, 2) if nearest_distance is not None else None,
        "note": "This shows real hazards near your exact live location, not a pre-defined destination safe zone."
    })


'''

content = content[:insert_idx] + new_route + content[insert_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Added /api/geofence-live route successfully")
