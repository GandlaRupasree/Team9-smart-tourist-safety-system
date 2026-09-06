with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found, no change made")
    return content

# 1. Fix the outdated subtitle
old1 = "Simulate your position relative to a destination's safe zone."
new1 = "Checks your real device location against this destination's safe zone."
content = try_replace(content, old1, new1, "subtitle text")

# 2. Add a clarifying note inside the Outside Safe Zone alert
old2 = """{!geoResult.inside_safe_zone && (
                    <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                  )}"""
new2 = """{!geoResult.inside_safe_zone && (
                    <>
                      <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                      <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who are meant to be near the destination but have drifted outside its safe zone.</p>
                    </>
                  )}"""
content = try_replace(content, old2, new2, "clarifying note")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
