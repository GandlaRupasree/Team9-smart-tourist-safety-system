with open("clean_attraction_names.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "def is_clean_name(name):\n    return bool(name) and bool(LATIN_ONLY.match(name))"
new = "def is_clean_name(name):\n    return isinstance(name, str) and bool(name) and bool(LATIN_ONLY.match(name))"

if old in content:
    content = content.replace(old, new)
    print("OK: is_clean_name now handles non-string values")
else:
    print("WARNING: anchor not found")

with open("clean_attraction_names.py", "w", encoding="utf-8") as f:
    f.write(content)
