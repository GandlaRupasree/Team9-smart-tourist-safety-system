with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old = "        guests: bookingAdults + bookingChildren,"
new = "        adults: bookingAdults,\n        children: bookingChildren,"

if old in content:
    content = content.replace(old, new)
    print("OK: bookListing now sends adults/children separately")
else:
    print("WARNING: anchor not found")

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)
