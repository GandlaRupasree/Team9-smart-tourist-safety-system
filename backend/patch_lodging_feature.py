with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = 'best_months = dest.get("season", {}).get("best_months", [])'
end_marker = '"entry_fee": entry_fee\n    }])'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx) + len(end_marker)

new_block = """best_months = dest.get("season", {}).get("best_months", [])
    in_season = 1 if month in best_months else 0
    rating = dest.get("ratings", {}).get("avg", 4.0)
    review_count = dest.get("ratings", {}).get("count", 0)
    entry_fee = dest.get("entry_fee", 0)
    lodging_count = db.real_hotels.count_documents({"destination_name": destination_name})

    features = pd.DataFrame([{
        "hour": hour,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "is_festival": is_festival,
        "in_season": in_season,
        "rating": rating,
        "review_count": review_count,
        "entry_fee": entry_fee,
        "lodging_count": lodging_count
    }])"""

content = content[:start_idx] + new_block + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched route with lodging_count")
