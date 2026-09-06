import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(
    r'<button className="sos-send-btn" onClick=\{triggerSOS\} disabled=\{sosLoading\}>\s*'
    r'\{sosLoading \? "Sending Alert\.\.\." : "Send SOS Alert"\}\s*'
    r'</button>'
)

replacement = (
    '<div className="sos-hold-wrapper">\n'
    '                    <button\n'
    '                      className="sos-hold-btn"\n'
    '                      onMouseDown={handleSosHoldStart}\n'
    '                      onMouseUp={handleSosHoldEnd}\n'
    '                      onMouseLeave={handleSosHoldEnd}\n'
    '                      onTouchStart={handleSosHoldStart}\n'
    '                      onTouchEnd={handleSosHoldEnd}\n'
    '                      disabled={sosLoading}\n'
    '                    >\n'
    '                      <span className="sos-hold-fill" style={{ height: `${sosHoldProgress}%` }}></span>\n'
    '                      <span className="sos-hold-label">{sosLoading ? "Sending..." : "SOS"}</span>\n'
    '                    </button>\n'
    '                    <p className="sos-hold-hint">Press and hold for 3 seconds to send an alert</p>\n'
    '                  </div>'
)

new_content, count = pattern.subn(replacement, content)

if count == 0:
    print("WARNING: button pattern not found")
else:
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: button replaced ({count} match)")
