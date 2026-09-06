with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def get_itinerary():"
end_marker = '@app.route("/api/real-hotels")'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_function = """def get_itinerary():
    destination_name = request.args.get("destination")
    duration_days = int(request.args.get("duration_days", 3))

    if not destination_name:
        return jsonify({"error": "destination parameter is required"}), 400

    dest = db.destinations.find_one({"name": destination_name})
    if not dest:
        return jsonify({"error": "destination not found"}), 404

    attractions = list(dest.get("attractions", []))
    hidden_gems = [f"(Hidden Gem) {g}" for g in dest.get("hidden_gems", [])]
    name = dest["name"]

    real_spots = attractions + hidden_gems
    has_real_spots = len(real_spots) > 0

    idx_pointer = [0]
    seen_once = set()

    def next_spot():
        if not has_real_spots:
            return "Explore the local area (no verified attractions listed for this destination yet)"
        spot = real_spots[idx_pointer[0] % len(real_spots)]
        is_repeat = spot in seen_once
        seen_once.add(spot)
        idx_pointer[0] += 1
        return f"Revisit - {spot}" if is_repeat else spot

    plan = []
    for day_num in range(1, duration_days + 1):
        if day_num == 1:
            title = f"Day 1 - Arrival in {name}"
        elif day_num == duration_days and duration_days > 1:
            title = f"Day {day_num} - Departure from {name}"
        else:
            title = f"Day {day_num} in {name}"

        if day_num == 1:
            morning = [
                "9:00 AM - Breakfast",
                "10:00 AM - Arrive and check into accommodation",
                f"11:00 AM - {next_spot()}",
                "1:00 PM - Lunch"
            ]
            afternoon = [
                f"2:30 PM - {next_spot()}",
                "4:00 PM - Free time / local exploration",
                "5:30 PM - Rest before dinner"
            ]
            night = [
                "7:00 PM - Try local cuisine for dinner",
                "8:30 PM - Relax at your accommodation"
            ]
        elif day_num == duration_days and duration_days > 1:
            morning = [
                "7:30 AM - Breakfast",
                f"8:30 AM - {next_spot()}",
                "10:30 AM - Free time / optional shopping"
            ]
            afternoon = [
                "12:30 PM - Lunch",
                "2:00 PM - Check out of accommodation",
                "3:00 PM - Head back / departure prep"
            ]
            night = [
                "Evening - Begin your return journey"
            ]
        else:
            morning = [
                "7:30 AM - Breakfast",
                f"8:30 AM - {next_spot()}",
                "12:30 PM - Lunch"
            ]
            afternoon = [
                f"2:00 PM - {next_spot()}",
                "4:30 PM - Free time / local exploration"
            ]
            night = [
                "7:00 PM - Dinner",
                "8:30 PM - Relax / optional evening activity"
            ]

        plan.append({
            "day": day_num,
            "title": title,
            "morning": morning,
            "afternoon": afternoon,
            "night": night
        })

    return jsonify({
        "destination": dest["name"],
        "duration_days": duration_days,
        "itinerary": plan,
        "verified_attraction_count": len(real_spots)
    })


"""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched get_itinerary successfully")
