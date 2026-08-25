with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def book_accommodation():"
end_marker = 'return jsonify(booking)'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx) + len(end_marker)

new_function = """def book_accommodation():
    data = request.get_json()
    accommodation_id = data.get("accommodation_id")
    source = data.get("source", "synthetic")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    adults = int(data.get("adults", 1))
    children = int(data.get("children", 0))
    device_id = data.get("device_id")

    if not accommodation_id:
        return jsonify({"error": "accommodation_id is required"}), 400
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400
    if not check_in or not check_out:
        return jsonify({"error": "check_in and check_out dates are required"}), 400
    if adults < 1:
        return jsonify({"error": "at least 1 adult is required"}), 400

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "check_in and check_out must be in YYYY-MM-DD format"}), 400

    nights = (check_out_date - check_in_date).days
    if nights < 1:
        return jsonify({"error": "check_out must be at least 1 day after check_in"}), 400

    guests = adults + children

    if source == "real":
        listing = db.real_hotels.find_one({"_id": ObjectId(accommodation_id)})
        if not listing:
            return jsonify({"error": "hotel not found"}), 404
        hotel_name = listing["hotel_name"]
        destination = listing["destination_name"]
        hotel_type = listing.get("tourism_type", "hotel")
        price_per_night = listing.get("estimated_price_per_night", 2000)
        address = listing.get("address", "")
    else:
        listing = db.accommodations.find_one({"_id": ObjectId(accommodation_id)})
        if not listing:
            return jsonify({"error": "accommodation not found"}), 404
        hotel_name = listing["name"]
        destination = listing["destination_name"]
        hotel_type = listing["type"]
        price_per_night = listing["price_per_night"]
        address = ""

    total_cost = price_per_night * nights
    booking_id = "TS" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    booking = {
        "booking_id": booking_id,
        "device_id": device_id,
        "accommodation_name": hotel_name,
        "destination": destination,
        "type": hotel_type,
        "address": address,
        "source": source,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "adults": adults,
        "children": children,
        "guests": guests,
        "price_per_night": price_per_night,
        "total_cost": total_cost,
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db.bookings.insert_one(booking)
    booking.pop("_id", None)
    return jsonify(booking)"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched book_accommodation successfully")
