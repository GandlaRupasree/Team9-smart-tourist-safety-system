import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

const INTEREST_OPTIONS = ["Adventure", "Nature", "Historical Places", "Beaches", "Wildlife", "Religious Tourism", "Shopping"]
const ACC_TYPES = ["Hotel", "Hostel", "Resort", "Homestay"]

function getDeviceId() {
  let id = localStorage.getItem("touresafe_device_id")
  if (!id) {
    id = "dev_" + Math.random().toString(36).slice(2) + Date.now().toString(36)
    localStorage.setItem("touresafe_device_id", id)
  }
  return id
}

function App() {
  const deviceId = getDeviceId()

  const [destinations, setDestinations] = useState([])
  const [displayLimit, setDisplayLimit] = useState(12)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [maxBudget, setMaxBudget] = useState(6000)
  const [maxDistance, setMaxDistance] = useState(3500)
  const [seasonOnly, setSeasonOnly] = useState(false)
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('score')

  const [crowdDestination, setCrowdDestination] = useState('')
  const [crowdDate, setCrowdDate] = useState('')
  const [crowdHour, setCrowdHour] = useState(12)
  const [crowdResult, setCrowdResult] = useState(null)
  const [crowdLoading, setCrowdLoading] = useState(false)
  const [crowdError, setCrowdError] = useState(null)

  const [planBudget, setPlanBudget] = useState(20000)
  const [planDuration, setPlanDuration] = useState(3)
  const [planInterests, setPlanInterests] = useState([])
  const [planTravelers, setPlanTravelers] = useState(2)
  const [planAgeGroup, setPlanAgeGroup] = useState('Adult')
  const [planTransport, setPlanTransport] = useState('Train')
  const [planAccommodation, setPlanAccommodation] = useState('Hotel')
  const [planResults, setPlanResults] = useState([])
  const [planLoading, setPlanLoading] = useState(false)
  const [planError, setPlanError] = useState(null)
  const [planSearched, setPlanSearched] = useState(false)

  const [itinerary, setItinerary] = useState(null)
  const [itineraryLoading, setItineraryLoading] = useState(false)
  const [itineraryError, setItineraryError] = useState(null)

  const [accModalOpen, setAccModalOpen] = useState(false)
  const [accDestination, setAccDestination] = useState(null)
  const [accType, setAccType] = useState('Hotel')
  const [accListings, setAccListings] = useState([])
  const [accLoading, setAccLoading] = useState(false)
  const [accError, setAccError] = useState(null)
  const [bookingConfirmation, setBookingConfirmation] = useState(null)
  const [bookingCheckIn, setBookingCheckIn] = useState('')
  const [bookingCheckOut, setBookingCheckOut] = useState('')
  const [bookingAdults, setBookingAdults] = useState(2)
  const [bookingChildren, setBookingChildren] = useState(0)
  const [realHotels, setRealHotels] = useState([])
  const [hasRealData, setHasRealData] = useState(false)
  const [attractionModalOpen, setAttractionModalOpen] = useState(false)
  const [attractionDestination, setAttractionDestination] = useState(null)

  const [bookingsOpen, setBookingsOpen] = useState(false)
  const [myBookings, setMyBookings] = useState([])
  const [bookingsLoading, setBookingsLoading] = useState(false)
  const [bookingsError, setBookingsError] = useState(null)
  const [bookingsSummary, setBookingsSummary] = useState(null)

  const [sosOpen, setSosOpen] = useState(false)
  const [sosDestination, setSosDestination] = useState('')
  const [sosSituation, setSosSituation] = useState('')
  const [sosLocationNote, setSosLocationNote] = useState('')
  const [sosResult, setSosResult] = useState(null)
  const [sosLoading, setSosLoading] = useState(false)
  const [sosError, setSosError] = useState(null)
  const [sosHoldProgress, setSosHoldProgress] = useState(0)
  const sosHoldTimerRef = useRef(null)

  const [geoOpen, setGeoOpen] = useState(false)
  const [geoDestination, setGeoDestination] = useState('')
  const [geoDrift, setGeoDrift] = useState(0)
  const [geoResult, setGeoResult] = useState(null)
  const [geoLoading, setGeoLoading] = useState(false)
  const [geoError, setGeoError] = useState(null)

  const [safetyOpen, setSafetyOpen] = useState(false)
  const [safetyDestination, setSafetyDestination] = useState('')
  const [safetyInfo, setSafetyInfo] = useState(null)
  const [safetyLoading, setSafetyLoading] = useState(false)
  const [safetyError, setSafetyError] = useState(null)

  const [incidentOpen, setIncidentOpen] = useState(false)
  const [incidentDestination, setIncidentDestination] = useState('')
  const [incidentType, setIncidentType] = useState('Theft')
  const [incidentDescription, setIncidentDescription] = useState('')
  const [incidentSeverity, setIncidentSeverity] = useState('Medium')
  const [incidentResult, setIncidentResult] = useState(null)
  const [incidentLoading, setIncidentLoading] = useState(false)
  const [incidentError, setIncidentError] = useState(null)
  const [incidentFeed, setIncidentFeed] = useState([])
  const [incidentFeedLoading, setIncidentFeedLoading] = useState(false)

  const fetchRecommendations = () => {
    setLoading(true)
    setError(null)
    setDisplayLimit(12)
    axios.get('http://127.0.0.1:5000/api/recommendations', {
      params: { max_budget: maxBudget, max_distance: maxDistance, season_only: seasonOnly, search: search, sort_by: sortBy }
    })
      .then(response => {
        setDestinations(response.data)
        setLoading(false)
        if (response.data.length > 0 && !crowdDestination) {
          setCrowdDestination(response.data[0].name)
        }
      })
      .catch(err => {
        setError('Failed to load recommendations. Is the backend running?')
        setLoading(false)
        console.error(err)
      })
  }

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchCrowdPrediction = () => {
    if (!crowdDestination) return
    setCrowdLoading(true)
    setCrowdError(null)
    const params = { destination: crowdDestination, hour: crowdHour }
    if (crowdDate) params.date = crowdDate
    axios.get('http://127.0.0.1:5000/api/crowd-prediction', { params })
      .then(response => {
        setCrowdResult(response.data)
        setCrowdLoading(false)
      })
      .catch(err => {
        setCrowdError('Could not fetch crowd prediction.')
        setCrowdLoading(false)
        console.error(err)
      })
  }

  const toggleInterest = (interest) => {
    setPlanInterests(prev => prev.includes(interest) ? prev.filter(i => i !== interest) : [...prev, interest])
  }

  const fetchSmartPlan = () => {
    setPlanLoading(true)
    setPlanError(null)
    setPlanSearched(true)
    setItinerary(null)
    axios.post('http://127.0.0.1:5000/api/smart-recommendations', {
      budget: planBudget,
      duration_days: planDuration,
      interests: planInterests,
      num_travelers: planTravelers,
      age_group: planAgeGroup,
      transport: planTransport,
      accommodation: planAccommodation
    })
      .then(response => {
        setPlanResults(response.data)
        setPlanLoading(false)
      })
      .catch(err => {
        setPlanError('Could not generate trip plan. Is the backend running?')
        setPlanLoading(false)
        console.error(err)
      })
  }

  const fetchItinerary = (destinationName) => {
    setItineraryLoading(true)
    setItineraryError(null)
    setItinerary(null)
    axios.get('http://127.0.0.1:5000/api/itinerary', {
      params: { destination: destinationName, duration_days: planDuration }
    })
      .then(response => {
        setItinerary(response.data)
        setItineraryLoading(false)
      })
      .catch(err => {
        setItineraryError('Could not generate itinerary.')
        setItineraryLoading(false)
        console.error(err)
      })
  }

  const openAccommodations = (destinationName) => {
    setAccDestination(destinationName)
    setAccModalOpen(true)
    setBookingConfirmation(null)
    fetchAccommodations(destinationName, accType)
    axios.get('http://127.0.0.1:5000/api/real-hotels', { params: { destination: destinationName } })
      .then(response => {
        setHasRealData(response.data.has_real_data)
        setRealHotels(response.data.hotels)
      })
      .catch(() => {
        setHasRealData(false)
        setRealHotels([])
      })
  }

  const fetchAccommodations = (destinationName, type) => {
    setAccLoading(true)
    setAccError(null)
    axios.get('http://127.0.0.1:5000/api/accommodations', {
      params: { destination: destinationName, type: type }
    })
      .then(response => {
        setAccListings(response.data)
        setAccLoading(false)
      })
      .catch(err => {
        setAccError('Could not load accommodations.')
        setAccLoading(false)
        console.error(err)
      })
  }

  const changeAccType = (type) => {
    setAccType(type)
    fetchAccommodations(accDestination, type)
  }

  const bookListing = (listing, source = 'synthetic') => {
    axios.post('http://127.0.0.1:5000/api/book', {
      accommodation_id: listing._id,
      source: source,
      check_in: bookingCheckIn || new Date().toISOString().split('T')[0],
      check_out: bookingCheckOut,
      guests: bookingAdults + bookingChildren,
      device_id: deviceId
    })
      .then(response => {
        setBookingConfirmation(response.data)
      })
      .catch(err => {
        setAccError('Booking failed. Please try again.')
        console.error(err)
      })
  }

  const closeAccModal = () => {
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
  }

  const openAttractions = (dest) => {
    setAttractionDestination(dest)
    setAttractionModalOpen(true)
  }

  const closeAttractionsModal = () => {
    setAttractionModalOpen(false)
    setAttractionDestination(null)
  }

  const fetchMyBookings = () => {
    setBookingsLoading(true)
    setBookingsError(null)
    axios.get('http://127.0.0.1:5000/api/bookings', { params: { device_id: deviceId } })
      .then(response => {
        setMyBookings(response.data)
        setBookingsLoading(false)
      })
      .catch(err => {
        setBookingsError('Could not load bookings.')
        setBookingsLoading(false)
        console.error(err)
      })
  }

  const fetchBookingsSummary = () => {
    axios.get('http://127.0.0.1:5000/api/bookings/summary', { params: { device_id: deviceId } })
      .then(response => {
        setBookingsSummary(response.data)
      })
      .catch(err => {
        console.error(err)
      })
  }

  const openMyBookings = () => {
    setBookingsOpen(true)
    fetchMyBookings()
    fetchBookingsSummary()
  }

  const cancelBooking = (bookingId) => {
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
  }

  const triggerSOS = () => {
    setSosLoading(true)
    setSosError(null)

    const sendAlert = (lat, lng) => {
      axios.post('http://127.0.0.1:5000/api/sos', {
        destination: sosDestination,
        situation: sosSituation || 'General emergency',
        location_note: sosLocationNote,
        lat: lat,
        lng: lng
      })
        .then(response => {
          setSosResult(response.data)
          setSosLoading(false)
        })
        .catch(err => {
          setSosError('Could not send SOS alert. Try calling emergency services directly.')
          setSosLoading(false)
          console.error(err)
        })
    }

    if (!navigator.geolocation) {
      sendAlert(null, null)
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        sendAlert(position.coords.latitude, position.coords.longitude)
      },
      () => {
        // Location denied or unavailable - still send the alert, just without coordinates
        sendAlert(null, null)
      },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  const handleSosHoldStart = () => {
    if (sosLoading) return
    let progress = 0
    sosHoldTimerRef.current = setInterval(() => {
      progress += 100 / (3000 / 50)
      if (progress >= 100) {
        clearInterval(sosHoldTimerRef.current)
        sosHoldTimerRef.current = null
        setSosHoldProgress(0)
        triggerSOS()
        return
      }
      setSosHoldProgress(progress)
    }, 50)
  }

  const handleSosHoldEnd = () => {
    if (sosHoldTimerRef.current) {
      clearInterval(sosHoldTimerRef.current)
      sosHoldTimerRef.current = null
    }
    setSosHoldProgress(0)
  }

  const closeSosModal = () => {
    setSosOpen(false)
    setSosResult(null)
    setSosSituation('')
    setSosLocationNote('')
    handleSosHoldEnd()
  }

  const checkGeofence = () => {
    if (!geoDestination) {
      setGeoError('Please select a destination.')
      return
    }
    if (!navigator.geolocation) {
      setGeoError('Geolocation is not supported by your browser.')
      return
    }

    setGeoLoading(true)
    setGeoError(null)
    setGeoResult(null)

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords
        axios.post('http://127.0.0.1:5000/api/geofence-check', {
          destination: geoDestination,
          lat: latitude,
          lng: longitude
        })
          .then(response => {
            setGeoResult(response.data)
            setGeoLoading(false)
          })
          .catch(err => {
            setGeoError('Could not check geofence.')
            setGeoLoading(false)
            console.error(err)
          })
      },
      (error) => {
        setGeoLoading(false)
        if (error.code === error.PERMISSION_DENIED) {
          setGeoError('Location permission denied. Allow location access in your browser to check your safety status.')
        } else {
          setGeoError('Could not get your location: ' + error.message)
        }
      },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  const closeGeoModal = () => {
    setGeoOpen(false)
    setGeoResult(null)
    setGeoDrift(0)
  }

  const fetchIncidentFeed = () => {
    setIncidentFeedLoading(true)
    axios.get('http://127.0.0.1:5000/api/incidents')
      .then(response => {
        setIncidentFeed(response.data)
        setIncidentFeedLoading(false)
      })
      .catch(err => {
        setIncidentFeedLoading(false)
        console.error(err)
      })
  }

  const openIncidentModal = () => {
    setIncidentOpen(true)
    setIncidentResult(null)
    fetchIncidentFeed()
  }

  const submitIncident = () => {
    if (!incidentDestination) {
      setIncidentError('Please select a destination.')
      return
    }
    setIncidentLoading(true)
    setIncidentError(null)
    axios.post('http://127.0.0.1:5000/api/incidents', {
      destination: incidentDestination,
      incident_type: incidentType,
      description: incidentDescription,
      severity: incidentSeverity
    })
      .then(response => {
        setIncidentResult(response.data)
        setIncidentLoading(false)
        setIncidentDescription('')
        fetchIncidentFeed()
      })
      .catch(err => {
        setIncidentError('Could not submit report.')
        setIncidentLoading(false)
        console.error(err)
      })
  }

  const closeIncidentModal = () => {
    setIncidentOpen(false)
    setIncidentResult(null)
  }

  const fetchSafetyInfo = (destinationName) => {
    if (!destinationName) return
    setSafetyLoading(true)
    setSafetyError(null)
    axios.get('http://127.0.0.1:5000/api/safety-info', { params: { destination: destinationName } })
      .then(response => {
        setSafetyInfo(response.data)
        setSafetyLoading(false)
      })
      .catch(err => {
        setSafetyError('Could not load safety info for this destination.')
        setSafetyLoading(false)
        console.error(err)
      })
  }

  const openSafetyModal = () => {
    setSafetyOpen(true)
    setSafetyInfo(null)
    if (safetyDestination) fetchSafetyInfo(safetyDestination)
  }

  const changeSafetyDestination = (name) => {
    setSafetyDestination(name)
    fetchSafetyInfo(name)
  }

  const closeSafetyModal = () => {
    setSafetyOpen(false)
    setSafetyInfo(null)
    setSafetyError(null)
  }

  const crowdLevelColor = { Low: '#2e7d32', Medium: '#f5a623', High: '#d32f2f' }

  const renderTimeBlock = (label, items) => {
    if (!items || items.length === 0) return null
    return (
      <div className="day-block">
        <h4 className="day-block-title">{label}</h4>
        <ul>
          {items.map((act, j) => (
            <li key={j} className={act.includes('(Local Tip)') ? 'hidden-gem-item' : ''}>
              {act.includes('(Local Tip)') && <span className="gem-badge">Local Tip</span>}
              {act.replace('(Local Tip) ', '')}
            </li>
          ))}
        </ul>
      </div>
    )
  }

  return (
    <div className="app-container">
      <div className="top-bar">
        <h1>Plan Your Trip</h1>
        <button className="apply-btn bookings-btn" onClick={openMyBookings}>My Bookings</button>
        <button className="sos-btn" onClick={() => setSosOpen(true)}>SOS</button>
        <button className="geo-btn" onClick={() => setGeoOpen(true)}>Geo-Fence Check</button>
        <button className="incident-btn" onClick={openIncidentModal}>Report Incident</button>
        <button className="safety-btn" onClick={openSafetyModal}>Nearby Help</button>
      </div>

      <div className="filters-panel plan-panel">
        <div className="filter-group">
          <label>Budget: Rs. {planBudget}</label>
          <input type="range" min="2000" max="100000" step="1000" value={planBudget} onChange={(e) => setPlanBudget(Number(e.target.value))} />
        </div>
        <div className="filter-group">
          <label>Duration: {planDuration} days</label>
          <input type="range" min="1" max="14" step="1" value={planDuration} onChange={(e) => setPlanDuration(Number(e.target.value))} />
        </div>
        <div className="filter-group">
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
        <div className="filter-group interests-group">
          <label>Interests</label>
          <div className="interest-chips">
            {INTEREST_OPTIONS.map((interest) => (
              <button key={interest} type="button" className={`chip ${planInterests.includes(interest) ? 'chip-active' : ''}`} onClick={() => toggleInterest(interest)}>
                {interest}
              </button>
            ))}
          </div>
        </div>
        <button className="apply-btn" onClick={fetchSmartPlan}>Find My Trip</button>
      </div>

      {planLoading && <div className="status-message">Finding the best destinations for you...</div>}
      {planError && <div className="status-message error">{planError}</div>}
      {planSearched && !planLoading && !planError && planResults.length === 0 && (
        <div className="status-message">No destinations match your plan. Try increasing your budget or duration.</div>
      )}

      {planResults.length > 0 && !planLoading && (
        <div className="card-grid">
          {planResults.map((dest, index) => (
            <div key={index} className="destination-card">
              <img src={dest.image_url} alt={dest.name} className="destination-image" loading="lazy" onError={(e) => { e.target.onerror = null; e.target.src = `https://picsum.photos/seed/${dest.name.replace(/\s/g, "")}fallback/400/300` }} />
              <h2>{dest.name}</h2>
              <p className="rating">Rating: {dest.rating} / 5</p>
              <p><strong>Distance:</strong> {dest.distance_km} km</p>
              <p><strong>Recommended Stay:</strong> {dest.recommended_days}</p>
              <p><strong>Estimated Total Cost:</strong> Rs. {dest.estimated_total_cost}</p>
              <p><strong>Cost / Person:</strong> Rs. {dest.cost_per_person}</p>
              <p className={dest.in_season ? 'in-season' : 'off-season'}>{dest.in_season ? 'In Season' : 'Off Season'}</p>
              <div className="attractions"><strong>Matches:</strong> {dest.interests.join(', ')}</div>
              <p className="score">Score: {dest.score}</p>
              {dest.sustainability_label && (
                <span className={`sustainability-badge sustainability-${dest.sustainability_score >= 75 ? 'high' : dest.sustainability_score >= 50 ? 'medium' : 'low'}`}>
                  {dest.sustainability_label} ({dest.sustainability_score})
                </span>
              )}
              <button className="itinerary-btn" onClick={() => fetchItinerary(dest.name)}>View Itinerary</button>
              <button className="itinerary-btn acc-btn" onClick={() => openAccommodations(dest.name)}>View Accommodations</button>
                <button className="itinerary-btn attractions-btn" onClick={() => openAttractions(dest)}>View Attractions</button>
            </div>
          ))}
        </div>
      )}

      {itineraryLoading && <div className="status-message">Building your itinerary...</div>}
      {itineraryError && <div className="status-message error">{itineraryError}</div>}

      {itinerary && !itineraryLoading && (
        <div className="itinerary-panel">
          <h2>{itinerary.destination} - {itinerary.duration_days} Day Itinerary</h2>
          <div className="itinerary-days">
            {itinerary.itinerary.map((day, i) => (
              <div key={i} className="itinerary-day-card">
                <h3>Day {day.day} - {day.title}</h3>
                {renderTimeBlock('Morning', day.morning)}
                {renderTimeBlock('Afternoon', day.afternoon)}
                {renderTimeBlock('Night', day.night)}
              </div>
            ))}
          </div>
        </div>
      )}

      <h1 className="crowd-heading">All Destinations</h1>
      <p className="results-count">Showing {Math.min(displayLimit, destinations.length)} of {destinations.length} destinations</p>
      {loading && <div className="status-message">Loading destinations...</div>}
      {error && <div className="status-message error">{error}</div>}
      {!loading && !error && destinations.length > 0 && (
        <>
        <div className="card-grid">
          {destinations.slice(0, displayLimit).map((dest, index) => (
            <div key={index} className="destination-card">
              <img
                src={dest.image_url}
                alt={dest.name}
                className="destination-image"
                loading="lazy"
                onError={(e) => { e.target.onerror = null; e.target.src = `https://picsum.photos/seed/${dest.name.replace(/\s/g, "")}fallback/400/300` }}
              />
              <h2>{dest.name}</h2>
              <p className="rating">Rating: {dest.rating} / 5</p>
              <p><strong>Distance:</strong> {dest.distance_km} km</p>
              <p><strong>Entry Fee:</strong> Rs. {dest.entry_fee}</p>
              <p><strong>Avg Cost:</strong> Rs. {dest.avg_cost}</p>
              <p className={dest.in_season ? "in-season" : "off-season"}>{dest.in_season ? "In Season" : "Off Season"}</p>
              <div className="attractions">
                <strong>Top Attractions:</strong>
                <ul>{dest.attractions.map((attr, i) => <li key={i}>{attr}</li>)}</ul>
              </div>
              <p className="score">Score: {dest.score}</p>
              {dest.sustainability_label && (
                <span className={`sustainability-badge sustainability-${dest.sustainability_score >= 75 ? "high" : dest.sustainability_score >= 50 ? "medium" : "low"}`}>
                  {dest.sustainability_label} ({dest.sustainability_score})
                </span>
              )}
              <button className="itinerary-btn" onClick={() => fetchItinerary(dest.name)}>View Itinerary</button>
              <button className="itinerary-btn acc-btn" onClick={() => openAccommodations(dest.name)}>View Accommodations</button>
                <button className="itinerary-btn attractions-btn" onClick={() => openAttractions(dest)}>View Attractions</button>
            </div>
          ))}
        </div>
        {displayLimit < destinations.length && (
          <button className="apply-btn load-more-btn" onClick={() => setDisplayLimit(prev => prev + 12)}>Load More Destinations</button>
        )}
        </>
      )}

      <h1 className="crowd-heading">Crowd Prediction</h1>

      <div className="filters-panel">
        <div className="filter-group">
          <label>Destination</label>
          <select value={crowdDestination} onChange={(e) => setCrowdDestination(e.target.value)}>
            {destinations.map((dest, i) => <option key={i} value={dest.name}>{dest.name}</option>)}
          </select>
        </div>
        <div className="filter-group">
          <label>Date</label>
          <input type="date" value={crowdDate} onChange={(e) => setCrowdDate(e.target.value)} />
        </div>
        <div className="filter-group">
          <label>Hour: {crowdHour}:00</label>
          <input type="range" min="6" max="20" step="1" value={crowdHour} onChange={(e) => setCrowdHour(Number(e.target.value))} />
        </div>
        <button className="apply-btn" onClick={fetchCrowdPrediction}>Check Crowd</button>
      </div>

      {crowdLoading && <div className="status-message">Checking crowd levels...</div>}
      {crowdError && <div className="status-message error">{crowdError}</div>}

      {crowdResult && !crowdLoading && (
        <div className="crowd-result-card">
          <h2>{crowdResult.destination}</h2>
          <p>{crowdResult.date} at {crowdResult.hour}:00</p>
          <div className="crowd-badge" style={{ backgroundColor: crowdLevelColor[crowdResult.crowd_level] }}>{crowdResult.crowd_level} Crowd</div>
          <p className="predicted-count">Predicted Visitors: ~{crowdResult.predicted_visitors}</p>
          <div className="crowd-details">
              {crowdResult.is_weekend && <span className="tag">Weekend</span>}
              {crowdResult.is_festival && <span className="tag">Festival</span>}
              {crowdResult.in_season && <span className="tag">In Season</span>}
            </div>
            {crowdResult.weather && (
              <p className="weather-note">
                {crowdResult.weather.condition}
                {crowdResult.weather.rain_probability != null && ` (${crowdResult.weather.rain_probability}% rain chance)`}
              </p>
            )}
          </div>
        )}
        {accModalOpen && (
        <div className="modal-overlay" onClick={closeAccModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeAccModal}>Close</button>
            <h2>Accommodations in {accDestination}</h2>

            <div className="booking-inputs">
              <div className="filter-group">
                <label>Check-in Date</label>
                <input type="date" value={bookingCheckIn} onChange={(e) => setBookingCheckIn(e.target.value)} />
              </div>
              <div className="filter-group">
                <label>Check-out Date</label>
                <input type="date" value={bookingCheckOut} onChange={(e) => setBookingCheckOut(e.target.value)} />
              </div>
              <div className="filter-group">
                <label>Adults</label>
                <input type="number" min="1" max="10" value={bookingAdults} onChange={(e) => setBookingAdults(Number(e.target.value))} />
              </div>
              <div className="filter-group">
                <label>Children</label>
                <input type="number" min="0" max="10" value={bookingChildren} onChange={(e) => setBookingChildren(Number(e.target.value))} />
              </div>
            </div>

            {hasRealData ? (
                <>
                  <div className="acc-list">
                    {realHotels.map((hotel) => (
                      <div key={hotel._id} className="acc-card real-hotel-card">
                        <div className="acc-card-header">
                          <h3>{hotel.hotel_name}</h3>
                          <span className="acc-rating">{hotel.rating || "N/A"} / 5</span>
                        </div>
                        <p className="acc-price">Rs. {hotel.estimated_price_per_night || "N/A"} / night (estimated)</p>
                        <p className="acc-amenities">{hotel.address}</p>
                        <p className="acc-amenities">Type: {hotel.tourism_type} - Phone: {hotel.phone}</p>
                        {hotel.estimated_price_per_night && bookingCheckIn && bookingCheckOut && bookingCheckOut > bookingCheckIn && (
                          <p className="acc-total">
                            Total for {Math.round((new Date(bookingCheckOut) - new Date(bookingCheckIn)) / 86400000)} nights: Rs. {hotel.estimated_price_per_night * Math.round((new Date(bookingCheckOut) - new Date(bookingCheckIn)) / 86400000)}
                          </p>
                        )}
                        <div className="real-hotel-actions">
                          <button
                            className="apply-btn small-btn"
                            onClick={() => bookListing(hotel, "real")}
                          >
                            Book Now
                          </button>
                          <a
                            className="apply-btn small-btn secondary-btn"
                            href={hotel.website || `https://www.google.com/maps/search/?api=1&query=${hotel.latitude},${hotel.longitude}`}
                            target="_blank"
                            rel="noreferrer"
                          >
                            Visit Hotel Page
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div className="status-message">No real hotel data available for this destination yet.</div>
              )}

              {bookingConfirmation && (
              <div className="booking-confirmation">
                <h3>Booking Confirmed!</h3>
                <p><strong>Booking ID:</strong> {bookingConfirmation.booking_id}</p>
                <p><strong>Property:</strong> {bookingConfirmation.accommodation_name}</p>
                <p><strong>Check-in:</strong> {bookingConfirmation.check_in}</p>
                <p><strong>Nights:</strong> {bookingConfirmation.nights}</p>
                <p><strong>Guests:</strong> {bookingConfirmation.guests}</p>
                <p><strong>Total Cost:</strong> Rs. {bookingConfirmation.total_cost}</p>
                <p className="booking-status">{bookingConfirmation.status}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {attractionModalOpen && attractionDestination && (
          <div className="modal-overlay" onClick={closeAttractionsModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={closeAttractionsModal}>Close</button>
              <h2>Attractions in {attractionDestination.name}</h2>
              <div className="attraction-gallery">
                {(attractionDestination.attraction_photos || attractionDestination.attractions.map(a => ({ name: a, image_url: null }))).map((photo, i) => (
                  <div key={i} className="attraction-card">
                    {photo.image_url ? (
                      <img
                        src={photo.image_url}
                        alt={photo.name}
                        className="attraction-image"
                        onError={(e) => { e.target.style.display = "none" }}
                      />
                    ) : (
                      <div className="attraction-image-placeholder">No photo available</div>
                    )}
                    <p className="attraction-name">{photo.name}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {bookingsOpen && (
        <div className="modal-overlay" onClick={() => setBookingsOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setBookingsOpen(false)}>Close</button>
            <h2>My Bookings</h2>

            {bookingsSummary && (
              <div className="summary-box">
                <div className="summary-stat">
                  <span className="summary-number">{bookingsSummary.total_bookings}</span>
                  <span className="summary-label">Active Bookings</span>
                </div>
                <div className="summary-stat">
                  <span className="summary-number">Rs. {bookingsSummary.total_spend}</span>
                  <span className="summary-label">Total Spend</span>
                </div>
                <div className="summary-stat">
                  <span className="summary-number">{bookingsSummary.total_nights}</span>
                  <span className="summary-label">Total Nights</span>
                </div>
                <div className="summary-stat">
                  <span className="summary-number">{bookingsSummary.destinations_count}</span>
                  <span className="summary-label">Destinations</span>
                </div>
              </div>
            )}

            {bookingsLoading && <div className="status-message">Loading your bookings...</div>}
            {bookingsError && <div className="status-message error">{bookingsError}</div>}
            {!bookingsLoading && !bookingsError && myBookings.length === 0 && (
              <div className="status-message">No bookings yet. Book an accommodation to see it here.</div>
            )}

            {!bookingsLoading && myBookings.length > 0 && (
              <div className="acc-list">
                {myBookings.map((booking) => (
                  <div key={booking._id} className="acc-card booking-card">
                    <div className="acc-card-header">
                      <h3>{booking.accommodation_name}</h3>
                      <span className="booking-id-tag">{booking.booking_id}</span>
                      </div>
                      <span className={booking.source === 'real' ? 'real-tag' : 'synthetic-tag'}>
                        {booking.source === 'real' ? 'Real Listing' : 'Sample Listing'}
                      </span>
                      <p><strong>Destination:</strong> {booking.destination} ({booking.type})</p>
                    <p><strong>Check-in:</strong> {booking.check_in} - <strong>Nights:</strong> {booking.nights} - <strong>Guests:</strong> {booking.guests}</p>
                    <p><strong>Total Cost:</strong> Rs. {booking.total_cost}</p>
                    <p className="booking-status">{booking.status}</p>
                    {booking.status === 'Confirmed' && (
                      <button className="cancel-btn" onClick={() => cancelBooking(booking.booking_id)}>Cancel Booking</button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {sosOpen && (
        <div className="modal-overlay" onClick={closeSosModal}>
          <div className="modal-content sos-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeSosModal}>Close</button>
            <h2 className="sos-title">Emergency SOS</h2>

            {!sosResult && (
              <>
                <div className="filter-group">
                  <label>Destination (optional)</label>
                  <select value={sosDestination} onChange={(e) => setSosDestination(e.target.value)}>
                    <option value="">Not sure / not listed</option>
                    {destinations.map((dest, i) => <option key={i} value={dest.name}>{dest.name}</option>)}
                  </select>
                </div>
                <div className="filter-group">
                  <label>What is happening?</label>
                  <textarea
                    className="sos-textarea"
                    placeholder="Briefly describe the situation..."
                    value={sosSituation}
                    onChange={(e) => setSosSituation(e.target.value)}
                  />
                </div>
                <div className="filter-group">
                  <label>Your location note (landmark, area, etc.)</label>
                  <input
                    type="text"
                    placeholder="e.g. near the main temple entrance"
                    value={sosLocationNote}
                    onChange={(e) => setSosLocationNote(e.target.value)}
                  />
                </div>
                {sosError && <div className="status-message error">{sosError}</div>}
                <button className="sos-send-btn" onClick={triggerSOS} disabled={sosLoading}>
                  {sosLoading ? "Sending Alert..." : "Send SOS Alert"}
                </button>
              </>
            )}

            {sosResult && (
              <div className="sos-confirmation">
                <h3>Alert Sent - {sosResult.alert.alert_id}</h3>
                <p>Status: {sosResult.alert.status}</p>
                <p>Time: {sosResult.alert.triggered_at}</p>
                  {sosResult.alert.lat && sosResult.alert.lng && (
                    <p>
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${sosResult.alert.lat},${sosResult.alert.lng}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        View my location on map
                      </a>
                    </p>
                  )}
                  {(!sosResult.alert.lat || !sosResult.alert.lng) && (
                    <p className="sos-no-location">Location was not available for this alert. Please state your location clearly if speaking with emergency services.</p>
                  )}
                <div className="emergency-contacts">
                  <h4>Emergency Contacts</h4>
                  <p>Police: {sosResult.emergency_contacts.police}</p>
                  <p>Ambulance: {sosResult.emergency_contacts.ambulance}</p>
                  <p>Fire: {sosResult.emergency_contacts.fire}</p>
                  <p>Tourist Helpline: {sosResult.emergency_contacts.tourist_helpline}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {geoOpen && (
        <div className="modal-overlay" onClick={closeGeoModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeGeoModal}>Close</button>
            <h2>Geo-Fence Safety Check</h2>
            <p className="geo-description">Checks your real device location against this destination's safe zone.</p>

            <div className="filter-group">
              <label>Destination</label>
              <select value={geoDestination} onChange={(e) => setGeoDestination(e.target.value)}>
                <option value="">Select a destination</option>
                {destinations.map((dest, i) => <option key={i} value={dest.name}>{dest.name}</option>)}
              </select>
            </div>

            <p className="status-message"></p>

              {geoError && <div className="status-message error">{geoError}</div>}

            <button className="apply-btn" onClick={checkGeofence}>Check Safety Status</button>

            {geoLoading && <div className="status-message">Checking...</div>}

            {geoResult && !geoLoading && (
              <div className={`geo-result-card ${geoResult.inside_safe_zone ? "geo-safe" : "geo-danger"}`}>
                <h3>{geoResult.status}</h3>
                <p><strong>Destination:</strong> {geoResult.destination}</p>
                <p><strong>Safe Zone Radius:</strong> {geoResult.safe_zone_radius_km} km</p>
                <p><strong>Distance from Center:</strong> {geoResult.distance_from_center_km} km</p>
                {!geoResult.inside_safe_zone && (
                  <>
                    <p className="geo-alert-id">Alert Triggered: {geoResult.alert_id}</p>
                    <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {incidentOpen && (
        <div className="modal-overlay" onClick={closeIncidentModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeIncidentModal}>Close</button>
            <h2>Report an Incident</h2>

            <div className="filter-group">
              <label>Destination</label>
              <select value={incidentDestination} onChange={(e) => setIncidentDestination(e.target.value)}>
                <option value="">Select a destination</option>
                {destinations.map((dest, i) => <option key={i} value={dest.name}>{dest.name}</option>)}
              </select>
            </div>

            <div className="filter-group">
              <label>Incident Type</label>
              <select value={incidentType} onChange={(e) => setIncidentType(e.target.value)}>
                <option>Theft</option>
                <option>Harassment</option>
                <option>Medical Emergency</option>
                <option>Natural Hazard</option>
                <option>Scam / Overcharging</option>
                <option>Other</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Severity</label>
              <select value={incidentSeverity} onChange={(e) => setIncidentSeverity(e.target.value)}>
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Description</label>
              <textarea
                className="sos-textarea"
                placeholder="Describe what happened..."
                value={incidentDescription}
                onChange={(e) => setIncidentDescription(e.target.value)}
              />
            </div>

            {incidentError && <div className="status-message error">{incidentError}</div>}

            <button className="apply-btn" onClick={submitIncident} disabled={incidentLoading}>
              {incidentLoading ? "Submitting..." : "Submit Report"}
            </button>

            {incidentResult && (
              <div className="incident-confirmation">
                <h3>Report Submitted - {incidentResult.report_id}</h3>
                <p>Status: {incidentResult.status}</p>
              </div>
            )}

            <h3 className="incident-feed-heading">Recent Incident Reports</h3>
            {incidentFeedLoading && <div className="status-message">Loading feed...</div>}
            {!incidentFeedLoading && incidentFeed.length === 0 && (
              <div className="status-message">No incidents reported yet.</div>
            )}
            {!incidentFeedLoading && incidentFeed.length > 0 && (
              <div className="acc-list">
                {incidentFeed.map((inc) => (
                  <div key={inc._id} className={`incident-card severity-${inc.severity.toLowerCase()}`}>
                    <div className="acc-card-header">
                      <h4>{inc.incident_type} - {inc.destination}</h4>
                      <span className="severity-tag">{inc.severity}</span>
                    </div>
                    {inc.description && <p>{inc.description}</p>}
                    <p className="incident-meta">{inc.reported_at} - {inc.status}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    {safetyOpen && (
      <div className="modal-overlay" onClick={closeSafetyModal}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <button className="modal-close" onClick={closeSafetyModal}>Close</button>
          <h2>Nearby Help</h2>
          <p className="geo-description">Real hospitals and police stations near your destination.</p>

          <div className="filter-group">
            <label>Destination</label>
            <select value={safetyDestination} onChange={(e) => changeSafetyDestination(e.target.value)}>
              <option value="">Select a destination</option>
              {destinations.map((dest, i) => <option key={i} value={dest.name}>{dest.name}</option>)}
            </select>
          </div>

          {safetyLoading && <div className="status-message">Loading nearby help...</div>}
          {safetyError && <div className="status-message error">{safetyError}</div>}

          {safetyInfo && !safetyLoading && (
            <>
              <div className="summary-box">
                <div className="summary-stat">
                  <span className="summary-number">{safetyInfo.emergency_contacts.police}</span>
                  <span className="summary-label">Police</span>
                </div>
                <div className="summary-stat">
                  <span className="summary-number">{safetyInfo.emergency_contacts.ambulance}</span>
                  <span className="summary-label">Ambulance</span>
                </div>
                <div className="summary-stat">
                  <span className="summary-number">{safetyInfo.emergency_contacts.fire}</span>
                  <span className="summary-label">Fire</span>
                </div>
                <div className="summary-stat">
                  <span className="summary-number">{safetyInfo.emergency_contacts.tourist_helpline}</span>
                  <span className="summary-label">Tourist Helpline</span>
                </div>
              </div>

              <h3 className="synthetic-title">Nearby Hospitals ({safetyInfo.hospitals.length})</h3>
              {safetyInfo.hospitals.length === 0 && <div className="status-message">No hospital data available nearby yet.</div>}
              <div className="acc-list">
                {safetyInfo.hospitals.map((h, i) => (
                  <div key={i} className="acc-card">
                    <div className="acc-card-header">
                      <h3>{h.name}</h3>
                      {h.distance_km != null && <span className="acc-rating">{h.distance_km} km</span>}
                    </div>
                    <p className="acc-amenities">{h.address}</p>
                    {h.lat && h.lon && (
                      <a className="apply-btn small-btn" href={`https://www.google.com/maps/dir/?api=1&destination=${h.lat},${h.lon}`} target="_blank" rel="noreferrer">
                        Directions
                      </a>
                    )}
                  </div>
                ))}
              </div>

              <h3 className="synthetic-title">Nearby Police Stations ({safetyInfo.police_stations.length})</h3>
              {safetyInfo.police_stations.length === 0 && <div className="status-message">No police station data available nearby yet.</div>}
              <div className="acc-list">
                {safetyInfo.police_stations.map((p, i) => (
                  <div key={i} className="acc-card">
                    <div className="acc-card-header">
                      <h3>{p.name}</h3>
                      {p.distance_km != null && <span className="acc-rating">{p.distance_km} km</span>}
                    </div>
                    <p className="acc-amenities">{p.address}</p>
                    {p.lat && p.lon && (
                      <a className="apply-btn small-btn" href={`https://www.google.com/maps/dir/?api=1&destination=${p.lat},${p.lon}`} target="_blank" rel="noreferrer">
                        Directions
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    )}
    </div>
  )
}

export default App












