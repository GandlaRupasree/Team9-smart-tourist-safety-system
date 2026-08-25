with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def get_dest_image(dest):"
end_marker = 'return f"https://picsum.photos/seed/{seed}/400/300"'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker, start_idx) + len(end_marker)

new_function = """def get_dest_image(dest):
    if dest.get("real_image_url"):
        return dest["real_image_url"]

    for photo in dest.get("attraction_photos", []):
        if photo.get("image_url"):
            return photo["image_url"]

    seed = dest["name"].replace(" ", "")
    return f"https://picsum.photos/seed/{seed}/400/300\""""

content = content[:start_idx] + new_function + content[end_idx:]

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched get_dest_image with attraction_photos fallback")
