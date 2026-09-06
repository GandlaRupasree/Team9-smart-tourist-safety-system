import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add geoMode state
old1 = "  const [geoUseLocation, setGeoUseLocation] = useState(true)"
new1 = old1 + "\n  const [geoMode, setGeoMode] = useState('destination')"
ok1 = old1 in content
content = content.replace(old1, new1, 1)

# 2. Replace checkGeofence function with two functions
pattern = re.compile(r"const checkGeofence = \(\) => \{.*?\n  \}", re.DOTALL)

new_functions = """const checkGeofenceByDestination = () => {
    if (!geoDestination) {
      setGeoError('Please select a destination.')
      return
    }
    setGeoLoading(true)
    setGeoError(null)
    setGeoResult(null)
    setGeoUserPos(null)

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
  }

  const checkGeofenceByLocation = () => {
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
            setGeoError('Could not check your location.')
            setGeoLoading(false)
            console.error(err)
          })
      },
      (error) => {
        setGeoLoading(false)
        if (error.code === error.PERMISSION_DENIED) {
          setGeoError('Location permission denied. Allow location access in your browser to use this mode.')
        } else {
          setGeoError('Could not get your location: ' + error.message)
        }
      },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }"""

new_content, count2 = pattern.subn(new_functions, content, count=1)

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"geoMode state added: {ok1}")
print(f"functions replaced: {count2 == 1}")
