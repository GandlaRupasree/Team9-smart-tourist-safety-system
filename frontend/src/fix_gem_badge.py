with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """<li key={j} className={act.includes('(Hidden Gem)') ? 'hidden-gem-item' : ''}>
              {act.includes('(Hidden Gem)') && <span className="gem-badge">Hidden Gem</span>}
              {act.replace('(Hidden Gem) ', '')}
            </li>"""
new = """<li key={j} className={act.includes('(Local Tip)') ? 'hidden-gem-item' : ''}>
              {act.includes('(Local Tip)') && <span className="gem-badge">Local Tip</span>}
              {act.replace('(Local Tip) ', '')}
            </li>"""

if old in content:
    content = content.replace(old, new)
    print("OK: badge relabeled")
else:
    print("WARNING: anchor not found - paste me the exact current block")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
