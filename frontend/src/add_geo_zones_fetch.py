import re

with open("App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add geoZones state after geoAlerts state
pattern1 = re.compile(r'(const \[geoAlerts, setGeoAlerts\] = useState\(\[\]\))')
content, n1 = pattern1.subn(r"\1\n  const [geoZones, setGeoZones] = useState(null)", content, count=1)

# 2. Fetch zones data inside checkGeofence, right after setGeoResult(response.data)
pattern2 = re.compile(
    r'(\.then\(response => \{\s*setGeoResult\(response\.data\)\s*setGeoLoading\(false\)\s*setGeoAlerts\(prev => \[[^\]]*?\]\.slice\(0, 5\)\)\s*\}\))'
)

addition = """
          axios.get(`http://127.0.0.1:5000/api/geofence-zones?destination=${geoDestination}`)
            .then(res => setGeoZones(res.data))
            .catch(() => setGeoZones(null))"""

def do_add(m):
    return m.group(1) + addition

content, n2 = pattern2.subn(do_add, content, count=1)

with open("App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print(f"geoZones state added: {n1 == 1}")
print(f"zones fetch added: {n2 == 1}")
