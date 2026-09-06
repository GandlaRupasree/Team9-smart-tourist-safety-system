with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

def try_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {label}")
    else:
        print(f"WARNING: {label} - anchor not found")
    return content

# 1. book_accommodation: require + store device_id
old1 = """    data = request.get_json()
    accommodation_id = data.get("accommodation_id")
    source = data.get("source", "synthetic")
    check_in = data.get("check_in")
    nights = int(data.get("nights", 1))
    guests = int(data.get("guests", 1))

    if not accommodation_id:
        return jsonify({"error": "accommodation_id is required"}), 400"""
new1 = """    data = request.get_json()
    accommodation_id = data.get("accommodation_id")
    source = data.get("source", "synthetic")
    check_in = data.get("check_in")
    nights = int(data.get("nights", 1))
    guests = int(data.get("guests", 1))
    device_id = data.get("device_id")

    if not accommodation_id:
        return jsonify({"error": "accommodation_id is required"}), 400
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400"""
content = try_replace(content, old1, new1, "book_accommodation params")

old2 = """    booking = {
        "booking_id": booking_id,
        "accommodation_name": hotel_name,
        "destination": destination,
        "type": hotel_type,
        "address": address,
        "source": source,
        "check_in": check_in,
        "nights": nights,
        "guests": guests,
        "price_per_night": price_per_night,
        "total_cost": total_cost,
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }"""
new2 = """    booking = {
        "booking_id": booking_id,
        "device_id": device_id,
        "accommodation_name": hotel_name,
        "destination": destination,
        "type": hotel_type,
        "address": address,
        "source": source,
        "check_in": check_in,
        "nights": nights,
        "guests": guests,
        "price_per_night": price_per_night,
        "total_cost": total_cost,
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }"""
content = try_replace(content, old2, new2, "booking dict includes device_id")

# 2. get_bookings: filter by device_id
old3 = '''@app.route("/api/bookings")
def get_bookings():
    bookings = list(db.bookings.find().sort("booked_at", -1))
    for b in bookings:
        b["_id"] = str(b["_id"])
    return jsonify(bookings)'''
new3 = '''@app.route("/api/bookings")
def get_bookings():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400
    bookings = list(db.bookings.find({"device_id": device_id}).sort("booked_at", -1))
    for b in bookings:
        b["_id"] = str(b["_id"])
    return jsonify(bookings)'''
content = try_replace(content, old3, new3, "get_bookings filtered")

# 3. bookings_summary: filter by device_id
old4 = '''@app.route("/api/bookings/summary")
def bookings_summary():
    confirmed = list(db.bookings.find({"status": "Confirmed"}))'''
new4 = '''@app.route("/api/bookings/summary")
def bookings_summary():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400
    confirmed = list(db.bookings.find({"status": "Confirmed", "device_id": device_id}))'''
content = try_replace(content, old4, new4, "bookings_summary filtered")

# 4. cancel_booking: verify ownership + refund estimate
old5 = '''@app.route("/api/bookings/cancel", methods=["POST"])
def cancel_booking():
    data = request.get_json()
    booking_id = data.get("booking_id")

    if not booking_id:
        return jsonify({"error": "booking_id is required"}), 400

    result = db.bookings.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": "Cancelled"}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "booking not found"}), 404

    return jsonify({"booking_id": booking_id, "status": "Cancelled"})'''
new5 = '''@app.route("/api/bookings/cancel", methods=["POST"])
def cancel_booking():
    data = request.get_json()
    booking_id = data.get("booking_id")
    device_id = data.get("device_id")

    if not booking_id:
        return jsonify({"error": "booking_id is required"}), 400
    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    booking = db.bookings.find_one({"booking_id": booking_id, "device_id": device_id})
    if not booking:
        return jsonify({"error": "booking not found"}), 404

    booked_at = datetime.strptime(booking["booked_at"], "%Y-%m-%d %H:%M:%S")
    hours_since_booking = (datetime.now() - booked_at).total_seconds() / 3600

    if hours_since_booking <= 24:
        refund_percent = 100
    else:
        refund_percent = 50

    refund_amount = round(booking["total_cost"] * refund_percent / 100)

    db.bookings.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": "Cancelled", "refund_percent": refund_percent, "refund_amount": refund_amount}}
    )

    return jsonify({
        "booking_id": booking_id,
        "status": "Cancelled",
        "refund_percent": refund_percent,
        "refund_amount": refund_amount
    })'''
content = try_replace(content, old5, new5, "cancel_booking with refund logic")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
