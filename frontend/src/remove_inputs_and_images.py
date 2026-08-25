with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old1 = """                <>
                  <div className="booking-inputs">
                    <div className="filter-group">
                      <label>Check-in Date</label>
                      <input type="date" value={bookingCheckIn} onChange={(e) => setBookingCheckIn(e.target.value)} />
                    </div>
                    <div className="filter-group">
                      <label>Nights</label>
                      <input type="number" min="1" max="30" value={bookingNights} onChange={(e) => setBookingNights(Number(e.target.value))} />
                    </div>
                    <div className="filter-group">
                      <label>Guests</label>
                      <input type="number" min="1" max="10" value={bookingGuests} onChange={(e) => setBookingGuests(Number(e.target.value))} />
                    </div>
                  </div>

                  <div className="acc-list">"""
new1 = """                <>
                  <div className="acc-list">"""

if old1 in content:
    content = content.replace(old1, new1)
    print("OK: booking inputs removed")
else:
    print("WARNING: booking-inputs block not found - no change made")

old2 = """                      <div key={hotel._id} className="acc-card real-hotel-card">
                        <img
                          src={hotel.image_url}
                          alt={hotel.hotel_name}
                          className="real-hotel-image"
                          onError={(e) => { e.target.style.display = "none" }}
                        />
                        <div className="acc-card-header">"""
new2 = """                      <div key={hotel._id} className="acc-card real-hotel-card">
                        <div className="acc-card-header">"""

if old2 in content:
    content = content.replace(old2, new2)
    print("OK: image tag removed")
else:
    print("WARNING: image block not found - no change made")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
