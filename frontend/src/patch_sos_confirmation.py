with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """<p>Time: {sosResult.alert.triggered_at}</p>"""
new = """<p>Time: {sosResult.alert.triggered_at}</p>
                  {sosResult.alert.lat && sosResult.alert.lng && (
                    <p>
                      
                        href={`https://www.google.com/maps/search/?api=1&query=${sosResult.alert.lat},${sosResult.alert.lng}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        View my location on map
                      </a>
                    </p>
                  )}
                  {(!sosResult.alert.lat || !sosResult.alert.lng) && (
                    <p className="sos-no-location">Location was not available for this alert. Please state your location clearly if speaking with emergency services.</p>
                  )}"""

if old in content:
    content = content.replace(old, new)
    print("OK: location display added to SOS confirmation")
else:
    print("WARNING: anchor not found - paste me Get-Content App.jsx | Select-String 'Time: {sosResult' -Context 2,2")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
