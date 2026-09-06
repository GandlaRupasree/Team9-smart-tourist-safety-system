with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """{geoAlerts.map((a, i) => (
                          <div key={i} className={`geo-alert-item ${a.inside_safe_zone ? 'geo-alert-safe' : 'geo-alert-warning'}`}>
                            <strong>{a.status}</strong> - {a.destination}
                            <div className="geo-alert-meta">{a.distance_from_center_km} km from center &middot; {a.time}</div>
                          </div>
                        ))}"""

new = """{geoAlerts.map((a, i) => (
                          a.live ? (
                            <div key={i} className="geo-alert-item geo-alert-safe">
                              <strong>Real-Time Check</strong> - near {a.destination || 'your location'}
                              <div className="geo-alert-meta">{a.nearest_distance_km != null ? `${a.nearest_distance_km} km from nearest saved destination` : 'Live GPS check'} &middot; {a.time}</div>
                            </div>
                          ) : (
                            <div key={i} className={`geo-alert-item ${a.inside_safe_zone ? 'geo-alert-safe' : 'geo-alert-warning'}`}>
                              <strong>{a.status}</strong> - {a.destination}
                              <div className="geo-alert-meta">{a.distance_from_center_km} km from center &middot; {a.time}</div>
                            </div>
                          )
                        ))}"""

if old in content:
    content = content.replace(old, new)
    print("OK: live-aware Recent Alerts")
else:
    print("WARNING: anchor not found")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
