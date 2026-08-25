with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """<p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                  <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>"""
new = """<>
                    <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                    <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                  </>"""

if old in content:
    content = content.replace(old, new)
    print("OK: wrapped in fragment")
else:
    print("WARNING: not found - paste me lines 850-865 with line numbers")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
