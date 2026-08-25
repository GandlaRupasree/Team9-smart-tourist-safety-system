with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "const checkGeofence = () => {"
end_marker = "const closeGeoModal = () => {"

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """const checkGeofence = () => {
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

  """

content = content[:start_idx] + new_function + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched checkGeofence to use real GPS")
