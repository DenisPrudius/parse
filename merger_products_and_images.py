import json

RESULTS_JSON = "results.json"
RESULTS_IMAGE_JSON = "results_image.json"
OUTPUT_JSON = "results_merged.json"

with open(RESULTS_JSON, "r", encoding="utf-8") as f:
    products = json.load(f)

with open(RESULTS_IMAGE_JSON, "r", encoding="utf-8") as f:
    images = json.load(f)

image_dict = {item["title"]: item.get("image") for item in images}

for product in products:
    title = product["title"]
    if title in image_dict:
        product["image"] = image_dict[title]
    else:
        product["image"] = None

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"✅ Об’єднано {len(products)} продуктів у {OUTPUT_JSON}")
