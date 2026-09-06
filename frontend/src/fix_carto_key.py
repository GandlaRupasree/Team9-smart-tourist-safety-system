with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = 'url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"'
new = 'url={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=${import.meta.env.VITE_CARTO_API_KEY}`}'

if old in content:
    content = content.replace(old, new)
    print("OK: tile URL now includes API key")
else:
    print("WARNING: anchor not found")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
