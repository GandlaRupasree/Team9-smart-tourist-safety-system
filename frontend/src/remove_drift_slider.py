with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """<div className="filter-group">
                <label>Simulated Drift from Safe Zone Center: {geoDrift} km</label>
                <input type="range" min="0" max="15" step="0.5" value={geoDrift} onChange={(e) => setGeoDrift(Number(e.target.value))} />
              </div>"""
new = """<p className="status-message">We will use your device's real GPS location when you check your status.</p>"""

if old in content:
    content = content.replace(old, new)
    print("OK: drift slider removed")
else:
    print("WARNING: slider block not found - paste me the exact current text and I will fix it")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
