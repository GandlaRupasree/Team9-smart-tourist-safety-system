with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Add a device ID helper right after the imports / before the component
old1 = "function App() {"
new1 = """function getDeviceId() {
  let id = localStorage.getItem("touresafe_device_id")
  if (!id) {
    id = "dev_" + Math.random().toString(36).slice(2) + Date.now().toString(36)
    localStorage.setItem("touresafe_device_id", id)
  }
  return id
}

function App() {
  const deviceId = getDeviceId()
"""
content = try_replace(content, old1, new1, "device ID helper + hook into App()")

# 2. bookListing sends device_id
old2 = """  const bookListing = (listing, source = 'synthetic') => {
    axios.post('http://127.0.0.1:5000/api/book', {
      accommodation_id: listing._id,
      source: source,
      check_in: bookingCheckIn || new Date().toISOString().split('T')[0],
      nights: bookingNights,
      guests: bookingGuests
    })"""
new2 = """  const bookListing = (listing, source = 'synthetic') => {
    axios.post('http://127.0.0.1:5000/api/book', {
      accommodation_id: listing._id,
      source: source,
      check_in: bookingCheckIn || new Date().toISOString().split('T')[0],
      nights: bookingNights,
      guests: bookingGuests,
      device_id: deviceId
    })"""
content = try_replace(content, old2, new2, "bookListing sends device_id")

# 3. fetchMyBookings sends device_id
old3 = """  const fetchMyBookings = () => {
    setBookingsLoading(true)
    setBookingsError(null)
    axios.get('http://127.0.0.1:5000/api/bookings')"""
new3 = """  const fetchMyBookings = () => {
    setBookingsLoading(true)
    setBookingsError(null)
    axios.get('http://127.0.0.1:5000/api/bookings', { params: { device_id: deviceId } })"""
content = try_replace(content, old3, new3, "fetchMyBookings sends device_id")

# 4. fetchBookingsSummary sends device_id
old4 = """  const fetchBookingsSummary = () => {
    axios.get('http://127.0.0.1:5000/api/bookings/summary')"""
new4 = """  const fetchBookingsSummary = () => {
    axios.get('http://127.0.0.1:5000/api/bookings/summary', { params: { device_id: deviceId } })"""
content = try_replace(content, old4, new4, "fetchBookingsSummary sends device_id")

# 5. cancelBooking: confirm dialog + device_id + refund message
old5 = """  const cancelBooking = (bookingId) => {
    axios.post('http://127.0.0.1:5000/api/bookings/cancel', { booking_id: bookingId })
      .then(() => {
        fetchMyBookings()
        fetchBookingsSummary()
      })
      .catch(err => {
        setBookingsError('Could not cancel booking.')
        console.error(err)
      })
  }"""
new5 = """  const cancelBooking = (bookingId) => {
    const confirmed = window.confirm("Cancel this booking? A refund (if applicable) will be estimated based on how long ago you booked.")
    if (!confirmed) return

    axios.post('http://127.0.0.1:5000/api/bookings/cancel', { booking_id: bookingId, device_id: deviceId })
      .then((response) => {
        alert(`Booking cancelled. Refund: Rs. ${response.data.refund_amount} (${response.data.refund_percent}%)`)
        fetchMyBookings()
        fetchBookingsSummary()
      })
      .catch(err => {
        setBookingsError('Could not cancel booking.')
        console.error(err)
      })
  }"""
content = try_replace(content, old5, new5, "cancelBooking confirm + refund")

# 6. Booking card: add real/synthetic badge
old6 = """                    <div key={booking._id} className="acc-card booking-card">
                      <div className="acc-card-header">
                        <h3>{booking.accommodation_name}</h3>
                        <span className="booking-id-tag">{booking.booking_id}</span>
                      </div>"""
new6 = """                    <div key={booking._id} className="acc-card booking-card">
                      <div className="acc-card-header">
                        <h3>{booking.accommodation_name}</h3>
                        <span className="booking-id-tag">{booking.booking_id}</span>
                      </div>
                      <span className={booking.source === 'real' ? 'real-tag' : 'synthetic-tag'}>
                        {booking.source === 'real' ? 'Real Listing' : 'Sample Listing'}
                      </span>"""
content = try_replace(content, old6, new6, "real/synthetic badge on booking card")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
