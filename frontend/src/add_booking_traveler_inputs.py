with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Add adult/children state next to the existing guest state
old1 = "const [bookingGuests, setBookingGuests] = useState(2)"
new1 = """const [bookingGuests, setBookingGuests] = useState(2)
  const [bookingAdults, setBookingAdults] = useState(2)
  const [bookingChildren, setBookingChildren] = useState(0)"""
content = try_replace(content, old1, new1, "add adult/children state")

# 2. Add the booking details form right under the modal title
old2 = "<h2>Accommodations in {accDestination}</h2>"
new2 = """<h2>Accommodations in {accDestination}</h2>

            <div className="booking-inputs">
              <div className="filter-group">
                <label>Nights</label>
                <input type="number" min="1" max="30" value={bookingNights} onChange={(e) => setBookingNights(Number(e.target.value))} />
              </div>
              <div className="filter-group">
                <label>Adults</label>
                <input type="number" min="1" max="10" value={bookingAdults} onChange={(e) => setBookingAdults(Number(e.target.value))} />
              </div>
              <div className="filter-group">
                <label>Children</label>
                <input type="number" min="0" max="10" value={bookingChildren} onChange={(e) => setBookingChildren(Number(e.target.value))} />
              </div>
            </div>"""
content = try_replace(content, old2, new2, "add booking details form")

# 3. Send adults + children as total guests when booking
old3 = """      nights: bookingNights,
      guests: bookingGuests,
      device_id: deviceId"""
new3 = """      nights: bookingNights,
      guests: bookingAdults + bookingChildren,
      device_id: deviceId"""
content = try_replace(content, old3, new3, "send adults+children as guests")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
