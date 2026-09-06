with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'attractions = list(dest.get("attractions", []))'
new = 'attractions = [a["name"] for a in dest.get("real_attractions", [])] or list(dest.get("attractions", []))'

if old in content:
    content = content.replace(old, new)
    print("OK: itinerary now uses real_attractions pool")
else:
    print("WARNING: anchor not found")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
