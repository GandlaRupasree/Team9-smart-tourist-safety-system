with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "const triggerSOS = () => {"
end_marker = "const closeSosModal = () => {"

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """const triggerSOS = () => {
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

  """

content = content[:start_idx] + new_function + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched triggerSOS to capture real GPS")
