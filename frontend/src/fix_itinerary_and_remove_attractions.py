import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label, count=1):
    n = content.count(old)
    if n >= count:
        content = content.replace(old, new, count)
        print(f"OK: {label} ({n} found, replaced {count})")
    else:
        print(f"WARNING: {label} - anchor not found (found {n}, needed {count})")
    return content

# 1. Update fetchItinerary to prompt for days
old1 = """const fetchItinerary = (destinationName) => {
    setItineraryLoading(true)
    setItineraryError(null)
    setItinerary(null)
    axios.get('http://127.0.0.1:5000/api/itinerary', {
      params: { destination: destinationName, duration_days: planDuration }
    })"""

new1 = """const fetchItinerary = (destinationName) => {
    const daysInput = window.prompt(`How many days is your trip to ${destinationName}?`, planDuration)
    if (!daysInput) return
    const numDays = parseInt(daysInput, 10)
    if (isNaN(numDays) || numDays < 1) {
      alert('Please enter a valid number of days.')
      return
    }
    setItineraryLoading(true)
    setItineraryError(null)
    setItinerary(null)
    axios.get('http://127.0.0.1:5000/api/itinerary', {
      params: { destination: destinationName, duration_days: numDays }
    })"""

content = try_replace(content, old1, new1, "fetchItinerary prompts for days")

# 2. Remove both "View Attractions" buttons
old2 = '''<button className="itinerary-btn attractions-btn" onClick={() => openAttractions(dest)}>View Attractions</button>
'''
new2 = ''
content = try_replace(content, old2, new2, "View Attractions buttons removed", count=2)

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
