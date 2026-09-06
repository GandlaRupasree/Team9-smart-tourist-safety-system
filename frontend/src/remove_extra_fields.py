with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

old = """          <div className="filter-group">
            <label>Travelers</label>
            <input type="number" min="1" max="20" value={planTravelers} onChange={(e) => setPlanTravelers(Number(e.target.value))} />
          </div>
          <div className="filter-group">
            <label>Age Group</label>
            <select value={planAgeGroup} onChange={(e) => setPlanAgeGroup(e.target.value)}>
              <option>Child</option><option>Youth</option><option>Adult</option><option>Senior</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Transportation</label>
            <select value={planTransport} onChange={(e) => setPlanTransport(e.target.value)}>
              <option>Bus</option><option>Train</option><option>Flight</option><option>Private Vehicle</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Accommodation</label>
            <select value={planAccommodation} onChange={(e) => setPlanAccommodation(e.target.value)}>
              <option>Hostel</option><option>Homestay</option><option>Hotel</option><option>Resort</option>
            </select>
          </div>
          <div className="filter-group interests-group">"""

new = """          <div className="filter-group interests-group">"""

content = try_replace(content, old, new, "removed Travelers/AgeGroup/Transportation/Accommodation fields")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
