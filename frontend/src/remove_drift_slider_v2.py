with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<label>Simulated Drift from Safe Zone Center"
end_marker = "{geoError &&"

start_idx = content.rindex("<div", 0, content.index(start_marker))
end_idx = content.index(end_marker, start_idx)

new_block = """<p className="status-message">We will use your device's real GPS location when you check your status.</p>

              """

content = content[:start_idx] + new_block + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed drift slider successfully")
