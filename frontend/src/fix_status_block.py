import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(
    r"<h3>\{geoResult\.status\}</h3>.*?safe zone\.</p>\s*"
    r"</>\s*"
    r"\)\}",
    re.DOTALL
)

new_block = """{geoResult.locationOff ? (
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

new_content, count = pattern.subn(new_block, content, count=1)

if count == 0:
    print("WARNING: pattern still not found")
else:
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: status block branched ({count} match)")
