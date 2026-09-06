with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Add state
old1 = "  const [incidentOpen, setIncidentOpen] = useState(false)"
new1 = """  const [safetyOpen, setSafetyOpen] = useState(false)
  const [safetyDestination, setSafetyDestination] = useState('')
  const [safetyInfo, setSafetyInfo] = useState(null)
  const [safetyLoading, setSafetyLoading] = useState(false)
  const [safetyError, setSafetyError] = useState(null)

  const [incidentOpen, setIncidentOpen] = useState(false)"""
content = try_replace(content, old1, new1, "safety state")

# 2. Add fetch + open/close functions right after closeIncidentModal
old2 = """  const closeIncidentModal = () => {
    setIncidentOpen(false)
    setIncidentResult(null)
  }"""
new2 = """  const closeIncidentModal = () => {
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
  }"""
content = try_replace(content, old2, new2, "safety functions")

# 3. Add the button next to Report Incident
old3 = '<button className="incident-btn" onClick={openIncidentModal}>Report Incident</button>'
new3 = '<button className="incident-btn" onClick={openIncidentModal}>Report Incident</button>\n        <button className="safety-btn" onClick={openSafetyModal}>Nearby Help</button>'
content = try_replace(content, old3, new3, "Nearby Help button")

# 4. Add the modal right before the closing </div> and export
old4 = "    </div>\n  )\n}\n\nexport default App"
new4 = """    {safetyOpen && (
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

export default App"""
content = try_replace(content, old4, new4, "safety modal")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
