with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Change outer map condition from geoUserPos to geoResult
old1 = "{geoUserPos && (() => {"
new1 = "{geoResult && (() => {"
content = try_replace(content, old1, new1, "outer map condition")

# 2. FitBounds points: only include user position if it exists
old2 = """<FitBounds points={[
                              [destLat, destLng],
                              [geoUserPos.lat, geoUserPos.lng],
                              ...zones.map(z => [z.lat, z.lng])
                            ]} />"""
new2 = """<FitBounds points={[
                              [destLat, destLng],
                              ...(geoUserPos ? [[geoUserPos.lat, geoUserPos.lng]] : []),
                              ...zones.map(z => [z.lat, z.lng])
                            ]} />"""
content = try_replace(content, old2, new2, "FitBounds conditional user point")

# 3. Only render the "you are here" marker if geoUserPos exists
old3 = """<Marker position={[geoUserPos.lat, geoUserPos.lng]} icon={youAreHereIcon}>
                              <Popup>You are here</Popup>
                            </Marker>"""
new3 = """{geoUserPos && (
                              <Marker position={[geoUserPos.lat, geoUserPos.lng]} icon={youAreHereIcon}>
                                <Popup>You are here</Popup>
                              </Marker>
                            )}"""
content = try_replace(content, old3, new3, "conditional you-are-here marker")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
