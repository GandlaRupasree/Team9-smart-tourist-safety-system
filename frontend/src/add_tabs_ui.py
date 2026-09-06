import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = '<p className="geo-description">'
end_marker = "{geoResult && !geoLoading && ("

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_block = """<p className="geo-description">Check safety status by destination or by your current location.</p>

              <div className="geo-mode-tabs">
                <button
                  className={`geo-mode-tab ${geoMode === 'destination' ? 'geo-mode-tab-active' : ''}`}
                  onClick={() => { setGeoMode('destination'); setGeoResult(null); setGeoError(null); setGeoUserPos(null) }}
                >
                  Enter Destination
                </button>
                <button
                  className={`geo-mode-tab ${geoMode === 'location' ? 'geo-mode-tab-active' : ''}`}
                  onClick={() => { setGeoMode('location'); setGeoResult(null); setGeoError(null) }}
                >
                  Use My Location
                </button>
              </div>

              {geoMode === 'destination' && (
                <div className="filter-group">
                  <label>Destination</label>
                  <select value={geoDestination} onChange={(e) => setGeoDestination(e.target.value)}>
                    <option value="">Select a destination</option>
                    {destinations.map((dest, i) => <option key={i} value={dest.name}>{dest.name}</option>)}
                  </select>
                </div>
              )}

              {geoMode === 'location' && (
                <p className="geo-location-hint">We'll use your device's real GPS location to find the nearest destination and check your safety status.</p>
              )}

              {geoError && <div className="status-message error">{geoError}</div>}

              {geoMode === 'destination' ? (
                <button className="apply-btn" onClick={checkGeofenceByDestination}>Check Safety Status</button>
              ) : (
                <button className="apply-btn" onClick={checkGeofenceByLocation}>Check My Location</button>
              )}

              {geoLoading && <div className="status-message">Checking...</div>}

              """

content = content[:start_idx] + new_block + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("OK: tabbed UI inserted")
