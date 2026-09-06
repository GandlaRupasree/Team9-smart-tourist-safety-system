with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Replace state: nights/guests -> checkIn/checkOut/adults/children
old1 = """  const [bookingNights, setBookingNights] = useState(2)
  const [bookingGuests, setBookingGuests] = useState(2)
  const [bookingCheckIn, setBookingCheckIn] = useState('')"""
new1 = """  const [bookingCheckIn, setBookingCheckIn] = useState('')
  const [bookingCheckOut, setBookingCheckOut] = useState('')
  const [bookingAdults, setBookingAdults] = useState(2)
  const [bookingChildren, setBookingChildren] = useState(0)
  const [bookingFormError, setBookingFormError] = useState(null)"""
content = try_replace(content, old1, new1, "booking state")

# 2. bookListing: send new fields, validate dates client-side too
old2 = """  const bookListing = (listing, source = 'synthetic') => {
    axios.post('http://127.0.0.1:5000/api/book', {
      accommodation_id: listing._id,
      source: source,
      check_in: bookingCheckIn || new Date().toISOString().split('T')[0],
      nights: bookingNights,
      guests: bookingGuests,
      device_id: deviceId
    })
      .then(response => {
        setBookingConfirmation(response.data)
      })
      .catch(err => {
        setAccError('Booking failed. Please try again.')
        console.error(err)
      })
  }"""
new2 = """  const bookListing = (listing, source = 'synthetic') => {
    setBookingFormError(null)
    if (!bookingCheckIn || !bookingCheckOut) {
      setBookingFormError('Please select both check-in and check-out dates.')
      return
    }
    if (bookingCheckOut <= bookingCheckIn) {
      setBookingFormError('Check-out date must be after check-in date.')
      return
    }
    axios.post('http://127.0.0.1:5000/api/book', {
      accommodation_id: listing._id,
      source: source,
      check_in: bookingCheckIn,
      check_out: bookingCheckOut,
      adults: bookingAdults,
      children: bookingChildren,
      device_id: deviceId
    })
      .then(response => {
        setBookingConfirmation(response.data)
      })
      .catch(err => {
        setAccError(err.response?.data?.error || 'Booking failed. Please try again.')
        console.error(err)
      })
  }"""
content = try_replace(content, old2, new2, "bookListing with dates + adults/children")

# 3. closeAccModal: reset new fields too
old3 = """  const closeAccModal = () => {
    setAccModalOpen(false)
    setAccDestination(null)
    setAccListings([])
    setBookingConfirmation(null)
    setRealHotels([])
    setHasRealData(false)
  }"""
new3 = """  const closeAccModal = () => {
    setAccModalOpen(false)
    setAccDestination(null)
    setAccListings([])
    setBookingConfirmation(null)
    setRealHotels([])
    setHasRealData(false)
    setBookingCheckIn('')
    setBookingCheckOut('')
    setBookingAdults(2)
    setBookingChildren(0)
    setBookingFormError(null)
  }"""
content = try_replace(content, old3, new3, "closeAccModal resets new fields")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
