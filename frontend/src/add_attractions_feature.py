with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found, no change made")
    return content

# 1. Add state for the attractions modal
old = "const [hasRealData, setHasRealData] = useState(false)"
new = """const [hasRealData, setHasRealData] = useState(false)
  const [attractionModalOpen, setAttractionModalOpen] = useState(false)
  const [attractionDestination, setAttractionDestination] = useState(null)"""
content = try_replace(content, old, new, "attraction modal state")

# 2. Add open/close functions right after closeAccModal
old = """    setRealHotels([])
    setHasRealData(false)
  }"""
new = """    setRealHotels([])
    setHasRealData(false)
  }

  const openAttractions = (dest) => {
    setAttractionDestination(dest)
    setAttractionModalOpen(true)
  }

  const closeAttractionsModal = () => {
    setAttractionModalOpen(false)
    setAttractionDestination(null)
  }"""
content = try_replace(content, old, new, "open/close attraction functions")

# 3. Add "View Attractions" button after every "View Accommodations" button
old = '<button className="itinerary-btn acc-btn" onClick={() => openAccommodations(dest.name)}>View Accommodations</button>'
new = old + '\n                <button className="itinerary-btn attractions-btn" onClick={() => openAttractions(dest)}>View Attractions</button>'
count = content.count(old)
content = content.replace(old, new)
print(f"OK: added View Attractions button in {count} place(s)" if count else "WARNING: View Accommodations button text not found")

# 4. Add the attractions gallery modal, right before the My Bookings modal
old = "{bookingsOpen && ("
new = """{attractionModalOpen && attractionDestination && (
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

        {bookingsOpen && ("""
content = try_replace(content, old, new, "attractions gallery modal")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
