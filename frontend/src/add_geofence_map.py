with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. Add Leaflet imports + default icon fix after existing imports
old1 = "import './App.css'"
new1 = """import './App.css'
import { MapContainer, TileLayer, Marker, Circle, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const youAreHereIcon = new L.Icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
})"""
content = try_replace(content, old1, new1, "leaflet imports + icon fix")

# 2. Add new state for user position + alert history
old2 = "  const [geoError, setGeoError] = useState(null)"
new2 = """  const [geoError, setGeoError] = useState(null)
  const [geoUserPos, setGeoUserPos] = useState(null)
  const [geoAlerts, setGeoAlerts] = useState([])"""
content = try_replace(content, old2, new2, "geoUserPos + geoAlerts state")

# 3. Capture user position when geolocation resolves
old3 = "        const { latitude, longitude } = position.coords"
new3 = """        const { latitude, longitude } = position.coords
        setGeoUserPos({ lat: latitude, lng: longitude })"""
content = try_replace(content, old3, new3, "capture user position")

# 4. Push result into alert history when response comes back
old4 = """          .then(response => {
            setGeoResult(response.data)
            setGeoLoading(false)
          })"""
new4 = """          .then(response => {
            setGeoResult(response.data)
            setGeoLoading(false)
            setGeoAlerts(prev => [
              {
                ...response.data,
                time: new Date().toLocaleTimeString()
              },
              ...prev
            ].slice(0, 5))
          })"""
content = try_replace(content, old4, new4, "push into alert history")

# 5. Insert the map + alerts panel after the alert-note paragraph block
old5 = """                    <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                    </>
                  )}"""
new5 = """                    <p className="geo-alert-note">This is expected if you are testing from somewhere other than {geoResult.destination}. Alerts are meant for travelers who have drifted outside a destination's safe zone.</p>
                    </>
                  )}

                  {geoUserPos && (() => {
                    const destObj = destinations.find(d => d.name === geoResult.destination)
                    const destLat = destObj?.location?.lat
                    const destLng = destObj?.location?.lng
                    if (!destLat || !destLng) return null
                    return (
                      <div className="geo-map-wrapper">
                        <MapContainer
                          center={[destLat, destLng]}
                          zoom={12}
                          style={{ height: '300px', width: '100%', borderRadius: '10px', marginTop: '12px' }}
                        >
                          <TileLayer
                            attribution='&copy; OpenStreetMap contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                          />
                          <Circle
                            center={[destLat, destLng]}
                            radius={geoResult.safe_zone_radius_km * 1000}
                            pathOptions={{ color: '#2ecc71', fillColor: '#2ecc71', fillOpacity: 0.15 }}
                          />
                          <Marker position={[destLat, destLng]}>
                            <Popup>{geoResult.destination} (Safe Zone Center)</Popup>
                          </Marker>
                          <Marker position={[geoUserPos.lat, geoUserPos.lng]} icon={youAreHereIcon}>
                            <Popup>You are here</Popup>
                          </Marker>
                        </MapContainer>
                      </div>
                    )
                  })()}

                  {geoAlerts.length > 0 && (
                    <div className="geo-alerts-panel">
                      <h4>Recent Alerts</h4>
                      {geoAlerts.map((a, i) => (
                        <div key={i} className={`geo-alert-item ${a.inside_safe_zone ? 'geo-alert-safe' : 'geo-alert-warning'}`}>
                          <strong>{a.status}</strong> - {a.destination}
                          <div className="geo-alert-meta">{a.distance_from_center_km} km from center &middot; {a.time}</div>
                        </div>
                      ))}
                    </div>
                  )}"""
content = try_replace(content, old5, new5, "map + alerts panel")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
