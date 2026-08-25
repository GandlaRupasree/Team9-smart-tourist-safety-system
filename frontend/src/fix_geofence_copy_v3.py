with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = "<p className=\"geo-alert-id\">Alert Triggered: {geoResult.alert_id}</p>"
new = old + "\n                  <p className=\"geo-alert-note\">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>"

if old in content:
    content = content.replace(old, new)
    print("OK: clarifying note added")
else:
    print("WARNING: still not found - paste me the exact current line and I will fix it")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
