with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<a\n"
end_marker_search = '''
                            className="apply-btn small-btn book-now-link"
                            href={hotel.website || `https://www.google.com/maps/search/?api=1&query=${hotel.latitude},${hotel.longitude}`}
                            target="_blank"
                            rel="noreferrer"
                          >
                            Book Now
                          </a>'''

new_block = '''<div className="real-hotel-actions">
                            <button
                              className="apply-btn small-btn"
                              onClick={() => bookListing(hotel, "real")}
                            >
                              Book Now
                            </button>
                            
                              className="apply-btn small-btn secondary-btn"
                              href={hotel.website || `https://www.google.com/maps/search/?api=1&query=${hotel.latitude},${hotel.longitude}`}
                              target="_blank"
                              rel="noreferrer"
                            >
                              Visit Hotel Page
                            </a>
                          </div>'''

if end_marker_search in content:
    content = content.replace(end_marker_search, new_block)
    print("OK: real hotel booking button added")
else:
    print("WARNING: exact block not found - trying line-based approach")
    lines = content.split("\\n")
    for i, line in enumerate(lines):
        if "book-now-link" in line:
            print(f"Found book-now-link reference near line {i+1}: {line.strip()}")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
