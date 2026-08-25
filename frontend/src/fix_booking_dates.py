with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Replace bookingNights state with checkIn/checkOut
old1 = "const [bookingNights, setBookingNights] = useState(2)"
new1 = "const [bookingCheckIn, setBookingCheckIn] = useState('')\n  const [bookingCheckOut, setBookingCheckOut] = useState('')"
content = try_replace(content, old1, new1, "state: nights -> checkIn/checkOut")

# 2. bookListing: send check_in/check_out instead of nights
old2 = "        nights: bookingNights,"
new2 = "        check_in: bookingCheckIn,\n        check_out: bookingCheckOut,"
content = try_replace(content, old2, new2, "bookListing sends check_in/check_out")

# 3. Replace the Nights number input with two date inputs
old3 = '''<div className="filter-group">
                  <label>Nights</label>
                  <input type="number" min="1" max="30" value={bookingNights} onChange={(e) => setBookingNights(Number(e.target.value))} />
                </div>'''
new3 = '''<div className="filter-group">
                  <label>Check-in Date</label>
                  <input type="date" value={bookingCheckIn} onChange={(e) => setBookingCheckIn(e.target.value)} />
                </div>
                <div className="filter-group">
                  <label>Check-out Date</label>
                  <input type="date" value={bookingCheckOut} onChange={(e) => setBookingCheckOut(e.target.value)} />
                </div>'''
content = try_replace(content, old3, new3, "Nights input -> date pickers")

# 4. Fix the total-cost display to compute nights from the two dates
old4 = '''<p className="acc-total">Total for {bookingNights} nights: Rs. {hotel.estimated_price_per_night * bookingNights}</p>'''
new4 = '''{bookingCheckIn && bookingCheckOut && bookingCheckOut > bookingCheckIn && (
                          <p className="acc-total">
                            Total for {Math.round((new Date(bookingCheckOut) - new Date(bookingCheckIn)) / 86400000)} nights: Rs. {hotel.estimated_price_per_night * Math.round((new Date(bookingCheckOut) - new Date(bookingCheckIn)) / 86400000)}
                          </p>
                        )}'''
content = try_replace(content, old4, new4, "total cost uses dates")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
