with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

anchor = "book-now-link"
anchor_idx = content.index(anchor)

# Find the start of the <a tag (walk backward to the nearest "<a")
start_idx = content.rindex("<a", 0, anchor_idx)

# Find the end of this </a> (walk forward from the anchor)
end_idx = content.index("</a>", anchor_idx) + len("</a>")

new_block = """<div className="real-hotel-actions">
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
                        </div>"""

content = content[:start_idx] + new_block + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched real hotel Book Now button successfully")
