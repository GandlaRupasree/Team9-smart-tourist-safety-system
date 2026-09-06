with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found, no change made")
    return content

# 1. Add the clarifying note below the alert
old1 = """{!geoResult.inside_safe_zone && (
                    <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                  )}"""
new1 = """{!geoResult.inside_safe_zone && (
                    <>
                      <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                      <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                    </>
                  )}"""
content = try_replace(content, old1, new1, "clarifying note")

# 2. Remove the duplicate GPS line (subtitle already says this)
old2 = "We will use your device's real GPS location when you check your status."
new2 = ""
content = try_replace(content, old2, new2, "duplicate GPS line")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
