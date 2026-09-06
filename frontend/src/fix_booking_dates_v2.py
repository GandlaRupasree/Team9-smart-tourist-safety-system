with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

old1 = "        nights: bookingNights,"
new1 = "        check_out: bookingCheckOut,"
content = try_replace(content, old1, new1, "bookListing: nights -> check_out")

old2 = '''<div className="filter-group">
                  <label>Nights</label>
                  <input type="number" min="1" max="30" value={bookingNights} onChange={(e) => setBookingNights(Number(e.target.value))} />
                </div>'''
new2 = '''<div className="filter-group">
                  <label>Check-in Date</label>
                  <input type="date" value={bookingCheckIn} onChange={(e) => setBookingCheckIn(e.target.value)} />
                </div>
                <div className="filter-group">
                  <label>Check-out Date</label>
                  <input type="date" value={bookingCheckOut} onChange={(e) => setBookingCheckOut(e.target.value)} />
                </div>'''
content = try_replace(content, old2, new2, "Nights input -> date pickers")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
