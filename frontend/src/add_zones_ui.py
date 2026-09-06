with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """                  {geoUserPos && (() => {
                    const destLat = geoResult.dest_lat
                    const destLng = geoResult.dest_lng
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

new = """                  {geoUserPos && (() => {
                    const destLat = geoResult.dest_lat
                    const destLng = geoResult.dest_lng
                    if (!destLat || !destLng) return null
                    const zones = geoZones?.zones || []
                    const safeZones = zones.filter(z => z.type === 'safe')
                    const warningZones = zones.filter(z => z.type === 'warning')
                    const dangerZones = zones.filter(z => z.type === 'danger')
                    const zoneColors = { safe: '#2ecc71', warning: '#f1c40f', danger: '#e74c3c' }
                    return (
                      <>
                        <div className="geo-map-wrapper geo-map-dark">
                          <MapContainer
                            center={[destLat, destLng]}
                            zoom={12}
                            style={{ height: '320px', width: '100%', borderRadius: '10px', marginTop: '12px' }}
                          >
                            <TileLayer
                              attribution='&copy; OpenStreetMap contributors &copy; CARTO'
                              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            />
                            {zones.length > 0 ? (
                              zones.map((z, i) => (
                                <Circle
                                  key={i}
                                  center={[z.lat, z.lng]}
                                  radius={z.radius_km * 1000}
                                  pathOptions={{ color: zoneColors[z.type] || '#999', fillColor: zoneColors[z.type] || '#999', fillOpacity: 0.2 }}
                                >
                                  <Popup>
                                    <strong>{z.label}</strong><br />
                                    {z.type === 'safe' && (
                                      <>Crime Rate: {z.details?.crime_rate}<br />{z.details?.note}</>
                                    )}
                                    {z.type !== 'safe' && (
                                      <>{z.details?.reason}<br />{z.details?.advice}</>
                                    )}
                                  </Popup>
                                </Circle>
                              ))
                            ) : (
                              <Circle
                                center={[destLat, destLng]}
                                radius={geoResult.safe_zone_radius_km * 1000}
                                pathOptions={{ color: '#2ecc71', fillColor: '#2ecc71', fillOpacity: 0.15 }}
                              />
                            )}
                            <Marker position={[destLat, destLng]}>
                              <Popup>{geoResult.destination} (Safe Zone Center)</Popup>
                            </Marker>
                            <Marker position={[geoUserPos.lat, geoUserPos.lng]} icon={youAreHereIcon}>
                              <Popup>You are here</Popup>
                            </Marker>
                          </MapContainer>
                          <div className="geo-map-legend">
                            <div className="geo-legend-title">Zone Legend</div>
                            <div className="geo-legend-item"><span className="geo-dot geo-dot-safe"></span>Safe Zone</div>
                            <div className="geo-legend-item"><span className="geo-dot geo-dot-warning"></span>Warning Zone</div>
                            <div className="geo-legend-item"><span className="geo-dot geo-dot-danger"></span>Danger Zone</div>
                          </div>
                        </div>

                        {zones.length > 0 && (
                          <div className="geo-zone-panels">
                            {safeZones.length > 0 && (
                              <div className="geo-zone-panel geo-zone-panel-safe">
                                <h4>Safe Zones</h4>
                                {safeZones.map((z, i) => (
                                  <div key={i} className="geo-zone-card">
                                    <div className="geo-zone-card-title">{z.label}</div>
                                    <div className="geo-zone-card-line">Crime Rate: {z.details?.crime_rate}</div>
                                    <div className="geo-zone-card-line">{z.details?.note}</div>
                                  </div>
                                ))}
                              </div>
                            )}
                            {warningZones.length > 0 && (
                              <div className="geo-zone-panel geo-zone-panel-warning">
                                <h4>Warning Zones</h4>
                                {warningZones.map((z, i) => (
                                  <div key={i} className="geo-zone-card">
                                    <div className="geo-zone-card-title">{z.label}</div>
                                    <div className="geo-zone-card-line">{z.details?.reason}</div>
                                    <div className="geo-zone-card-line">{z.details?.advice}</div>
                                  </div>
                                ))}
                              </div>
                            )}
                            {dangerZones.length > 0 && (
                              <div className="geo-zone-panel geo-zone-panel-danger">
                                <h4>Danger Zones</h4>
                                {dangerZones.map((z, i) => (
                                  <div key={i} className="geo-zone-card">
                                    <div className="geo-zone-card-title">{z.label}</div>
                                    <div className="geo-zone-card-line">{z.details?.reason}</div>
                                    <div className="geo-zone-card-line">{z.details?.advice}</div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        )}
                      </>
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

if old in content:
    content = content.replace(old, new, 1)
    with open("App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: zones map + panels inserted")
else:
    print("WARNING: anchor not found")
