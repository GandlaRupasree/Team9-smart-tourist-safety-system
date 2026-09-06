with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<div className=\"crowd-details\">"
end_marker = "{accModalOpen && ("

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx)

new_block = """<div className="crowd-details">
              {crowdResult.is_weekend && <span className="tag">Weekend</span>}
              {crowdResult.is_festival && <span className="tag">Festival</span>}
              {crowdResult.in_season && <span className="tag">In Season</span>}
            </div>
            {crowdResult.weather && (
              <p className="weather-note">
                {crowdResult.weather.condition}
                {crowdResult.weather.rain_probability != null && ` (${crowdResult.weather.rain_probability}% rain chance)`}
              </p>
            )}
          </div>
        )}
        """

content = content[:start_idx] + new_block + content[end_idx:]

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched crowd result card successfully")
