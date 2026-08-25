with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def get_weather_adjustment(lat, lng, date_str):"
end_marker = "if lat is None or lng is None:"

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

fixed = """def get_weather_adjustment(lat, lng, date_str):
    # Live weather forecast -> a multiplier on predicted crowd size.
    # Open-Meteo is free, no API key. Forecasts only exist ~16 days ahead;
    # outside that window this safely returns a neutral 1.0 multiplier.
    """

content = content[:start_idx] + fixed + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed docstring")
