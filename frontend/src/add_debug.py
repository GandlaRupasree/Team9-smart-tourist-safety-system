import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = "if (!destLat || !destLng) return null"
new = """console.log('GEO DEBUG:', { geoUserPos, destinationsCount: destinations.length, destObj, destLat, destLng })
                    if (!destLat || !destLng) return null"""

if old in content:
    content = content.replace(old, new, 1)
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: debug line inserted")
else:
    print("WARNING: anchor not found")
