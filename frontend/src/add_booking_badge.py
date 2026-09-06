with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = """<span className="booking-id-tag">{booking.booking_id}</span>
                      </div>"""
new = """<span className="booking-id-tag">{booking.booking_id}</span>
                      </div>
                      <span className={booking.source === 'real' ? 'real-tag' : 'synthetic-tag'}>
                        {booking.source === 'real' ? 'Real Listing' : 'Sample Listing'}
                      </span>"""

if old in content:
    content = content.replace(old, new)
    print("OK: badge added")
else:
    print("WARNING: still not found - paste Get-Content App.jsx | Select-String 'booking-id-tag' -Context 2,2")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
