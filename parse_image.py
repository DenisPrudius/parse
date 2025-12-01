import json
import time
from dataclasses import dataclass, fields, asdict
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests


BASE_URL = "https://kitka-sonya.com/"
PARSE_URL = urljoin(BASE_URL, "shop")


@dataclass
class Product:
    title: str
    image: str


PRODUCT_FIELDS = [field.name for field in fields(Product)]

driver = webdriver.Chrome()
driver.get(PARSE_URL)
wait = WebDriverWait(driver, 8)

time.sleep(2)

while True:
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.woocommerce-load-more"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
        time.sleep(0.5)
        load_more.click()
        time.sleep(1.5)
    except:
        break


def get_product_links():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a.woocommerce-LoopProduct-link")
    return [link["href"] for link in links]


def parse_product_page(url):
    driver.get(url)
    WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "h1.product_title")
    )
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    img = soup.select_one(".woocommerce-product-gallery__image img")
    image = img["src"] if img else ""

    title_element = soup.select_one("h1.product_title")
    title = title_element.text.strip() if title_element else ""

    return Product(
        title=title,
        image=image,
    )


def write_to_json(products):
    data = [asdict(product) for product in products]
    with open("results_image.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def download_images(json_path="results_image.json", images_dir="images"):
    os.makedirs(images_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        img_url = item.get("image")

        if not img_url:
            print(f"No picture {item.get('title')}")
            continue

        img_name = img_url.split("/")[-1]
        save_path = os.path.join(images_dir, img_name)

        try:
            print(f" Download {img_name}...")
            response = requests.get(img_url, timeout=10)

            with open(save_path, "wb") as img_file:
                img_file.write(response.content)

            print(f"Saved: {save_path}")

        except Exception as e:
            print(f"Error {img_url}: {e}")


def main():
    product_links = get_product_links()
    print(f"Found {len(product_links)} products. Parsing...")

    products = []
    for url in product_links:
        product = parse_product_page(url)
        products.append(product)
        print(f"Parsed: {product.title}")

    write_to_json(products)
    print("JSON saved.")

    download_images()

    print(f"Done. Parsed {len(products)} products.")


if __name__ == "__main__":
    main()
