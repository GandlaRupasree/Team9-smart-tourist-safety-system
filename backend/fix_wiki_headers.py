with open("fetch_verified_photos.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'WIKI_URL = "https://en.wikipedia.org/w/api.php"'
new = '''WIKI_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "TourSafeStudentProject/1.0 (contact: student-project@example.com)"}'''

if old in content:
    content = content.replace(old, new)
    print("OK: added HEADERS")
else:
    print("WARNING: URL line not found")

old2 = "r = requests.get(WIKI_URL, params=params, timeout=REQUEST_TIMEOUT)"
new2 = "r = requests.get(WIKI_URL, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)"

if old2 in content:
    content = content.replace(old2, new2)
    print("OK: added headers to request")
else:
    print("WARNING: request line not found")

with open("fetch_verified_photos.py", "w", encoding="utf-8") as f:
    f.write(content)
