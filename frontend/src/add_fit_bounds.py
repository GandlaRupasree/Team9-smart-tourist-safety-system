import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add useMap import alongside other react-leaflet imports
old1 = "import { MapContainer, TileLayer, Marker, Circle, Popup } from 'react-leaflet'"
new1 = "import { MapContainer, TileLayer, Marker, Circle, Popup, useMap } from 'react-leaflet'"
ok1 = old1 in content
content = content.replace(old1, new1, 1)

# 2. Add a FitBounds helper component right after the youAreHereIcon definition
old2 = """const youAreHereIcon = new L.Icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
})"""

new2 = old2 + """

function FitBounds({ points }) {
  const map = useMap()
  useEffect(() => {
    if (points && points.length > 0) {
      const bounds = L.latLngBounds(points)
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 })
    }
  }, [JSON.stringify(points)])
  return null
}"""

ok2 = old2 in content
content = content.replace(old2, new2, 1)

# 3. Insert <FitBounds> inside the MapContainer, right after <TileLayer ... /> closing
old3 = '''url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            />'''
new3 = '''url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            />
                            <FitBounds points={[
                              [destLat, destLng],
                              [geoUserPos.lat, geoUserPos.lng],
                              ...zones.map(z => [z.lat, z.lng])
                            ]} />'''
ok3 = old3 in content
content = content.replace(old3, new3, 1)

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print(f"useMap import updated: {ok1}")
print(f"FitBounds component added: {ok2}")
print(f"FitBounds inserted in map: {ok3}")
