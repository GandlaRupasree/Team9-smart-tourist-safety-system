import joblib

model = joblib.load("crowd_model.pkl")
print("Model type:", type(model))

feature_names = ["hour", "day_of_week", "month", "is_weekend", "is_holiday",
                  "is_festival", "in_season", "rating", "review_count", "entry_fee"]

if hasattr(model, "feature_importances_"):
    importances = model.feature_importances_
    ranked = sorted(zip(feature_names, importances), key=lambda x: -x[1])
    print("\nFeature importance (higher = model relies on it more):")
    for name, score in ranked:
        bar = "#" * int(score * 50)
        print(f"  {name:15s} {score:.3f}  {bar}")
else:
    print("This model type doesn't expose feature_importances_ directly - tell me what type it printed above.")
