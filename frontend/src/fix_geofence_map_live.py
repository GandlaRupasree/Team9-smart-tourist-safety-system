with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

old1 = """                      const destLat = geoResult.dest_lat
                      const destLng = geoResult.dest_lng
                      if (!destLat || !destLng) return null"""
new1 = """                      const destLat = geoResult.live ? geoUserPos?.lat : geoResult.dest_lat
                      const destLng = geoResult.live ? geoUserPos?.lng : geoResult.dest_lng
                      if (!destLat || !destLng) return null"""
content = try_replace(content, old1, new1, "destLat/destLng handle live mode")

old2 = """                              ) : (
                                <Circle
                                  center={[destLat, destLng]}
                                  radius={geoResult.safe_zone_radius_km * 1000}
                                  pathOptions={{ color: '#2ecc71', fillColor: '#2ecc71', fillOpacity: 0.15 }}
                                />
                              )}"""
new2 = """                              ) : (
                                !geoResult.live && (
                                  <Circle
                                    center={[destLat, destLng]}
                                    radius={geoResult.safe_zone_radius_km * 1000}
                                    pathOptions={{ color: '#2ecc71', fillColor: '#2ecc71', fillOpacity: 0.15 }}
                                  />
                                )
                              )}"""
content = try_replace(content, old2, new2, "fallback safe circle skipped in live mode")

old3 = """                              <Marker position={[destLat, destLng]}>
                                <Popup>{geoResult.destination} (Safe Zone Center)</Popup>
                              </Marker>"""
new3 = """                              {!geoResult.live && (
                                <Marker position={[destLat, destLng]}>
                                  <Popup>{geoResult.destination} (Safe Zone Center)</Popup>
                                </Marker>
                              )}"""
content = try_replace(content, old3, new3, "destination marker skipped in live mode")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
