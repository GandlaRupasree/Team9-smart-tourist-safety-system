with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        if day_num == 1:
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
            ]"""
new = """        if day_num == 1:
            morning = [
                "9:00 AM - Breakfast",
                "10:00 AM - Arrive and check into accommodation",
                f"11:00 AM - {next_spot()}",
                "1:00 PM - Lunch"
            ]
            afternoon = [
                f"2:30 PM - {next_spot()}",
                "4:00 PM - Free time / local exploration"
            ]
            night = [
                f"6:00 PM - {next_spot()}",
                "7:30 PM - Try local cuisine for dinner",
                "9:00 PM - Relax at your accommodation"
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
                f"6:00 PM - {next_spot()}",
                "7:30 PM - Dinner",
                "9:00 PM - Relax / optional evening activity"
            ]"""

if old in content:
    content = content.replace(old, new)
    print("OK: added evening attraction slot")
else:
    print("WARNING: anchor not found")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
