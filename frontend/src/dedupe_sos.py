with open("App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

seen = set()
out = []
targets = [
    "const [sosHoldProgress, setSosHoldProgress] = useState(0)",
    "const sosHoldTimerRef = useRef(null)",
]

removed = 0
for line in lines:
    stripped = line.strip()
    if stripped in targets:
        if stripped in seen:
            removed += 1
            continue  # skip duplicate
        seen.add(stripped)
    out.append(line)

with open("App.jsx", "w", encoding="utf-8") as f:
    f.writelines(out)

print(f"Removed {removed} duplicate line(s)")
