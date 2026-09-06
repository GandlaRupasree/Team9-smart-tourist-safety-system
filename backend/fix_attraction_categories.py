with open("fetch_real_attractions.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'CATEGORIES = "tourism.sights,tourism.attraction,natural.water.waterfall,heritage"'
new = 'CATEGORIES = "tourism.sights,tourism.attraction,heritage,natural.water"'

if old in content:
    content = content.replace(old, new)
    print("OK: fixed categories")
else:
    print("WARNING: not found")

with open("fetch_real_attractions.py", "w", encoding="utf-8") as f:
    f.write(content)
