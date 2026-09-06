import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(
    r'(<p className="geo-alert-note">.*?drifted outside a destination\'s safe zone\.</p>\s*'
    r'</>\s*'
    r'\)\}\s*'
    r')(</div>\s*\)\})',
    re.DOTALL
)

addition = """
                  {geoUserPos && (() => {
                    const destObj = destinations.find(d => d.name === geoResult.destination)
                    const destLat = destObj?.location?.lat
                    const destLng = destObj?.location?.lng
                    if (!destLat || !destLng) return null
                    return (
                      <div className="geo-map-wrapper">
                        <MapContainer
                          center={[destLat, destLng]}
                          zoom={12}
                          style={{ height: '300px', width: '100%', borderRadius: '10px', marginTop: '12px' }}
                        >
                          <TileLayer
                            attribution='&copy; OpenStreetMap contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                          />
                          <Circle
                            center={[destLat, destLng]}
                            radius={geoResult.safe_zone_radius_km * 1000}
                            pathOptions={{ color: '#2ecc71', fillColor: '#2ecc71', fillOpacity: 0.15 }}
                          />
                          <Marker position={[destLat, destLng]}>
                            <Popup>{geoResult.destination} (Safe Zone Center)</Popup>
                          </Marker>
                          <Marker position={[geoUserPos.lat, geoUserPos.lng]} icon={youAreHereIcon}>
                            <Popup>You are here</Popup>
                          </Marker>
                        </MapContainer>
                      </div>
                    )
                  })()}

                  {geoAlerts.length > 0 && (
                    <div className="geo-alerts-panel">
                      <h4>Recent Alerts</h4>
                      {geoAlerts.map((a, i) => (
                        <div key={i} className={`geo-alert-item ${a.inside_safe_zone ? 'geo-alert-safe' : 'geo-alert-warning'}`}>
                          <strong>{a.status}</strong> - {a.destination}
                          <div className="geo-alert-meta">{a.distance_from_center_km} km from center &middot; {a.time}</div>
                        </div>
                      ))}
                    </div>
                  )}
                """

def do_replace(m):
    return m.group(1) + addition + m.group(2)

new_content, count = pattern.subn(do_replace, content)

if count == 0:
    print("WARNING: pattern still not found")
else:
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: map + alerts panel inserted ({count} match)")
