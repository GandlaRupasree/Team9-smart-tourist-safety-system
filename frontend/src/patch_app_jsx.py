with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "{hasRealData && ("
end_marker = "{bookingConfirmation && ("

start_idx = content.index(start_marker)
end_idx = content.index(end_marker)

new_block = """{hasRealData ? (
                <>
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

                  <div className="acc-list">
                    {realHotels.map((hotel) => (
                      <div key={hotel._id} className="acc-card real-hotel-card">
                        <img
                          src={hotel.image_url}
                          alt={hotel.hotel_name}
                          className="real-hotel-image"
                          onError={(e) => { e.target.style.display = "none" }}
                        />
                        <div className="acc-card-header">
                          <h3>{hotel.hotel_name}</h3>
                          <span className="acc-rating">{hotel.rating || "N/A"} / 5</span>
                        </div>
                        <p className="acc-price">Rs. {hotel.estimated_price_per_night || "N/A"} / night (estimated)</p>
                        <p className="acc-amenities">{hotel.address}</p>
                        <p className="acc-amenities">Type: {hotel.tourism_type} - Phone: {hotel.phone}</p>
                        {hotel.estimated_price_per_night && (
                          <p className="acc-total">Total for {bookingNights} nights: Rs. {hotel.estimated_price_per_night * bookingNights}</p>
                        )}
                        
                          className="apply-btn small-btn book-now-link"
                          href={hotel.website || `https://www.google.com/maps/search/?api=1&query=${hotel.latitude},${hotel.longitude}`}
                          target="_blank"
                          rel="noreferrer"
                        >
                          Book Now
                        </a>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div className="status-message">No real hotel data available for this destination yet.</div>
              )}

              """

content = content[:start_idx] + new_block + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched App.jsx successfully")
