with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

old1 = "axios.post('http://127.0.0.1:5000/api/geofence-nearest', {"
new1 = "axios.post('http://127.0.0.1:5000/api/geofence-live', {"
content = try_replace(content, old1, new1, "endpoint URL")

old2 = "            setGeoResult(response.data)"
new2 = """            setGeoResult({
              destination: response.data.nearest_destination || 'Your current location',
              status: 'Live Location Check',
              live: true,
              user_lat: response.data.user_lat,
              user_lng: response.data.user_lng,
              nearest_distance_km: response.data.nearest_distance_km,
              note: response.data.note
            })"""
content = try_replace(content, old2, new2, "geoResult shape for live mode")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
