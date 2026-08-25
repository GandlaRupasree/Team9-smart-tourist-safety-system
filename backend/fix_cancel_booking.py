with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def cancel_booking():"
end_marker = '@app.route("/api/crowd-prediction")'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """def cancel_booking():
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
    })


"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched cancel_booking successfully")
