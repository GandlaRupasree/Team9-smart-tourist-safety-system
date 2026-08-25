with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "{booking.booking_id}</span>"
end_marker = "<p><strong>Destination:</strong>"

start_idx = content.index(start_marker) + len(start_marker)
end_idx = content.index(end_marker, start_idx)

badge = """
                      </div>
                      <span className={booking.source === 'real' ? 'real-tag' : 'synthetic-tag'}>
                        {booking.source === 'real' ? 'Real Listing' : 'Sample Listing'}
                      </span>
                      """

content = content[:start_idx] + badge + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Badge inserted successfully")
