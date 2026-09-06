import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

old1 = '<div className={`geo-result-card ${geoResult.inside_safe_zone ? "geo-safe" : "geo-danger"}`}>'
new1 = '<div className={`geo-result-card ${geoResult.locationOff ? "geo-neutral" : (geoResult.inside_safe_zone ? "geo-safe" : "geo-danger")}`}>'
content = try_replace(content, old1, new1, "result card class guarded")

old2 = """                  <h3>{geoResult.status}</h3>
                  <p><strong>Destination:</strong> {geoResult.destination}</p>
                  <p><strong>Safe Zone Radius:</strong> {geoResult.safe_zone_radius_km} km</p>
                  <p><strong>Distance from Center:</strong> {geoResult.distance_from_center_km} km</p>
                  {!geoResult.inside_safe_zone && (
                    <>
                      <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                      <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                    </>
                  )}"""

new2 = """                  {geoResult.locationOff ? (
                    <>
                      <h3>Zone Overview</h3>
                      <p><strong>Destination:</strong> {geoResult.destination}</p>
                      <p><strong>Safe Zone Radius:</strong> {geoResult.safe_zone_radius_km} km</p>
                      <p className="geo-alert-note">Location is off. Showing zone information for {geoResult.destination}. Turn on "Use my current location" to check your real safety status.</p>
                    </>
                  ) : (
                    <>
                      <h3>{geoResult.status}</h3>
                      <p><strong>Destination:</strong> {geoResult.destination}</p>
                      <p><strong>Safe Zone Radius:</strong> {geoResult.safe_zone_radius_km} km</p>
                      <p><strong>Distance from Center:</strong> {geoResult.distance_from_center_km} km</p>
                      {!geoResult.inside_safe_zone && (
                        <>
                          <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                          <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                        </>
                      )}
                    </>
                  )}"""

content = try_replace(content, old2, new2, "status block branched")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
