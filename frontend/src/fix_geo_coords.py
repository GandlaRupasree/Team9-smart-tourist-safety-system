with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """                  {geoUserPos && (() => {
                    const destObj = destinations.find(d => d.name === geoResult.destination)
                    const destLat = destObj?.location?.lat
                    const destLng = destObj?.location?.lng
                    console.log('GEO DEBUG:', { geoUserPos, destinationsCount: destinations.length, destObj, destLat, destLng })
                    if (!destLat || !destLng) return null"""

new = """                  {geoUserPos && (() => {
                    const destLat = geoResult.dest_lat
                    const destLng = geoResult.dest_lng
                    if (!destLat || !destLng) return null"""

if old in content:
    content = content.replace(old, new, 1)
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: frontend updated to use geoResult coordinates")
else:
    print("WARNING: anchor not found")
