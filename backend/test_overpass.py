import requests

query = """[out:json][timeout:25];
(
  node["tourism"~"hotel|hostel|guest_house"](around:8000,12.3375,75.8069);
);
out center 10;
"""

headers = {"User-Agent": "TourSafeStudentProject/1.0 (educational use)"}

r = requests.post("https://overpass-api.de/api/interpreter", data={"data": query}, headers=headers, timeout=25)
print("Status:", r.status_code)

if r.status_code == 200:
    data = r.json()
    print("Elements found:", len(data.get("elements", [])))
    for el in data.get("elements", [])[:5]:
        print(" -", el.get("tags", {}).get("name"))
else:
    print("Response text:", r.text[:500])
