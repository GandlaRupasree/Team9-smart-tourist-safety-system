import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(
    r'(\{geoError && <div className="status-message error">\{geoError\}</div>\}\s*)'
    r'(<button className="apply-btn" onClick=\{checkGeofence\}>Check Safety Status</button>)'
)

addition = '''<div className="geo-location-toggle">
                <label className="geo-toggle-label">
                  <input
                    type="checkbox"
                    checked={geoUseLocation}
                    onChange={(e) => setGeoUseLocation(e.target.checked)}
                  />
                  Use my current location
                </label>
                <p className="geo-toggle-hint">
                  {geoUseLocation
                    ? "We'll check your real device location against this destination's zones."
                    : "We'll just show this destination's zone map, without checking your location."}
                </p>
              </div>
              '''

def do_add(m):
    return m.group(1) + addition + m.group(2)

new_content, count = pattern.subn(do_add, content, count=1)

if count == 0:
    print("WARNING: anchor not found")
else:
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: toggle UI inserted ({count} match)")
