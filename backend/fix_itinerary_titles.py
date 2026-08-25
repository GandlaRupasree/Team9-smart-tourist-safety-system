with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

old1 = 'title = f"Day 1 - Arrival in {name}"'
new1 = 'title = f"Arrival in {name}"'
content = try_replace(content, old1, new1, "day 1 title")

old2 = 'title = f"Day {day_num} - Departure from {name}"'
new2 = 'title = f"Departure from {name}"'
content = try_replace(content, old2, new2, "final day title")

old3 = 'title = f"Day {day_num} in {name}"'
new3 = 'title = f"Exploring {name}"'
content = try_replace(content, old3, new3, "middle day title")

old4 = 'hidden_gems = [f"(Hidden Gem) {g}" for g in dest.get("hidden_gems", [])]'
new4 = 'hidden_gems = [f"(Local Tip) {g}" for g in dest.get("hidden_gems", [])]'
content = try_replace(content, old4, new4, "hidden gem relabel")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
