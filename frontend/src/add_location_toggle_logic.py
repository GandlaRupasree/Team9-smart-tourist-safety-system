with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Add geoUseLocation state
old1 = "  const [geoZones, setGeoZones] = useState(null)"
new1 = """  const [geoZones, setGeoZones] = useState(null)
  const [geoUseLocation, setGeoUseLocation] = useState(true)"""
content = try_replace(content, old1, new1, "geoUseLocation state")

# 2. Replace checkGeofence with a version that branches on geoUseLocation
old2 = """  const checkGeofence = () => {
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
        setGeoUserPos({ lat: latitude, lng: longitude })
        axios.post('http://127.0.0.1:5000/api/geofence-check', {
          destination: geoDestination,
          lat: latitude,
          lng: longitude
        })
          .then(response => {
            setGeoResult(response.data)
            setGeoLoading(false)
            setGeoAlerts(prev => [
              {
                ...response.data,
                time: new Date().toLocaleTimeString()
              },
              ...prev
            ].slice(0, 5))
          })
          axios.get(`http://127.0.0.1:5000/api/geofence-zones?destination=${geoDestination}`)
            .then(res => setGeoZones(res.data))
            .catch(() => setGeoZones(null))
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
  }"""

new2 = """  const checkGeofence = () => {
    if (!geoDestination) {
      setGeoError('Please select a destination.')
      return
    }

    setGeoLoading(true)
    setGeoError(null)
    setGeoResult(null)
    setGeoUserPos(null)

    if (!geoUseLocation) {
      axios.get(`http://127.0.0.1:5000/api/geofence-zones?destination=${geoDestination}`)
        .then(res => {
          setGeoZones(res.data)
          setGeoResult({
            destination: geoDestination,
            locationOff: true,
            safe_zone_radius_km: res.data.safe_zone_radius_km,
            dest_lat: res.data.location?.lat,
            dest_lng: res.data.location?.lng
          })
          setGeoLoading(false)
        })
        .catch(err => {
          setGeoError('Could not load zone information.')
          setGeoLoading(false)
          console.error(err)
        })
      return
    }

    if (!navigator.geolocation) {
      setGeoError('Geolocation is not supported by your browser.')
      setGeoLoading(false)
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords
        setGeoUserPos({ lat: latitude, lng: longitude })
        axios.post('http://127.0.0.1:5000/api/geofence-check', {
          destination: geoDestination,
          lat: latitude,
          lng: longitude
        })
          .then(response => {
            setGeoResult(response.data)
            setGeoLoading(false)
            setGeoAlerts(prev => [
              {
                ...response.data,
                time: new Date().toLocaleTimeString()
              },
              ...prev
            ].slice(0, 5))
          })
          axios.get(`http://127.0.0.1:5000/api/geofence-zones?destination=${geoDestination}`)
            .then(res => setGeoZones(res.data))
            .catch(() => setGeoZones(null))
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
  }"""

content = try_replace(content, old2, new2, "checkGeofence branching logic")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
