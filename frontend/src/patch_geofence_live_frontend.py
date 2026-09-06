with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """  const checkGeofenceByLocation = () => {
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
        setGeoUserPos({ lat: latitude, lng: longitude })
        axios.post('http://127.0.0.1:5000/api/geofence-nearest', {
          lat: latitude,
          lng: longitude
        })
          .then(response => {
            setGeoResult(response.data)
            setGeoZones({ zones: response.data.zones || [] })
            setGeoLoading(false)
            setGeoAlerts(prev => [
              {
                ...response.data,
                time: new Date().toLocaleTimeString()
              },
              ...prev
            ].slice(0, 5))
          })
          .catch(err => {
            setGeoError('Could not check your location.')"""

new = """  const checkGeofenceByLocation = () => {
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
        setGeoUserPos({ lat: latitude, lng: longitude })
        axios.post('http://127.0.0.1:5000/api/geofence-live', {
          lat: latitude,
          lng: longitude
        })
          .then(response => {
            const liveResult = {
              destination: response.data.nearest_destination || 'Your current location',
              status: 'Live Location Check',
              live: true,
              user_lat: response.data.user_lat,
              user_lng: response.data.user_lng,
              nearest_distance_km: response.data.nearest_distance_km,
              note: response.data.note
            }
            setGeoResult(liveResult)
            setGeoZones({ zones: response.data.zones || [] })
            setGeoLoading(false)
            setGeoAlerts(prev => [
              {
                ...liveResult,
                time: new Date().toLocaleTimeString()
              },
              ...prev
            ].slice(0, 5))
          })
          .catch(err => {
            setGeoError('Could not check your location.')"""

if old in content:
    content = content.replace(old, new)
    print("OK: checkGeofenceByLocation now uses live endpoint")
else:
    print("WARNING: anchor not found")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
