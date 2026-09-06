with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """                {geoResult && !geoLoading && (
                <div className={`geo-result-card ${geoResult.locationOff ? "geo-neutral" : (geoResult.inside_safe_zone ? "geo-safe" : "geo-danger")}`}>
                  {geoResult.locationOff ? (
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

new = """                {geoResult && !geoLoading && (
                <div className={`geo-result-card ${geoResult.live ? "geo-neutral" : (geoResult.locationOff ? "geo-neutral" : (geoResult.inside_safe_zone ? "geo-safe" : "geo-danger"))}`}>
                  {geoResult.live ? (
                      <>
                        <h3>Real-Time Safety Check</h3>
                        <p className="geo-alert-note">Showing real hazards from OpenStreetMap near your exact current location, updated live.</p>
                        {geoResult.nearest_distance_km != null && (
                          <p><strong>Nearest saved destination:</strong> {geoResult.destination} ({geoResult.nearest_distance_km} km away)</p>
                        )}
                      </>
                    ) : geoResult.locationOff ? (
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

if old in content:
    content = content.replace(old, new)
    print("OK: live-mode header added")
else:
    print("WARNING: anchor not found")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
