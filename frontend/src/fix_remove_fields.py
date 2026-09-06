import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(
    r'<div className="filter-group">\s*<label>Travelers</label>.*?'
    r'<div className="filter-group interests-group">',
    re.DOTALL
)

replacement = '<div className="filter-group interests-group">'

new_content, count = pattern.subn(replacement, content, count=1)

if count == 0:
    print("WARNING: pattern not found")
else:
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: fields removed ({count} match)")
