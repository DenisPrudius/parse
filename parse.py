import os
import json
import time
import re
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

BASE_URL = "https://kitka-sonya.com/"
PARSE_URL = urljoin(BASE_URL, "shop/")

@dataclass
class Product:
    title: str
    current_price: float | None
    old_price: float | None
    rating: float | None
    image_link: str
    description: dict
    image_path: str

def clean_price(price: str) -> float | None:
    if not price:
        return None
    price = (price.
             replace(" ", "").
             replace("грн", "").
             replace("\u20b4", "").
             replace(",", ".")
             )
    try:
        return float(price)
    except ValueError:
        return None

def parse_description(soup: BeautifulSoup) -> dict:
    tab = soup.select_one("#tab-additional_information table")
    if not tab:
        return {}
    result = {}
    for row in tab.select("tr"):
        key = row.select_one("th")
        val = row.select_one("td")
        if key and val:
            result[key.text.strip()] = val.text.strip()
    return result

def download_image(url: str, folder: str = "images"):
    if not url:
        return ""
    os.makedirs(folder, exist_ok=True)
    filename = url.split("/")[-1].split("?")[0]
    path = os.path.join(folder, filename)
    response = requests.get(url)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)
    return path

def parse_product_page(driver, url: str) -> Product:
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, "h1.product_title"))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    title_el = soup.select_one(".product_title.entry-title")
    title = title_el.text.strip() if title_el else ""

    price_block = soup.select_one(".product_price, .summary .price")
    if price_block:
        current_price_element = price_block.select_one("span.woocommerce-Price-amount:not(del .woocommerce-Price-amount)")
        old_price_el = price_block.select_one("del .woocommerce-Price-amount")
        current_price = clean_price(current_price_element.text.strip()) if current_price_element else None
        old_price = clean_price(old_price_el.text.strip()) if old_price_el else None
    else:
        current_price = old_price = None

    rating_element = soup.select_one(".star-rating")
    if rating_element and rating_element.get("aria-label"):
        match = re.search(r"([\d\.]+)", rating_element["aria-label"])
        rating = float(match.group(1)) if match else None
    else:
        rating = None

    image_element = soup.select_one(".woocommerce-product-gallery__image img, .wp-post-image")
    image_link = image_element["src"] if image_element else ""
    image_path = download_image(image_link) if image_link else ""

    description = parse_description(soup)

    return Product(
        title=title,
        current_price=current_price,
        old_price=old_price,
        rating=rating,
        image_link=image_link,
        image_path=image_path,
        description=description
    )

def get_all_product_links(driver):
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    links = [a["href"] for a in soup.select("a[href*='/продукт/']") if a.get("href")]
    return list(set(links))

def main():
    driver = webdriver.Chrome()
    driver.get(PARSE_URL)
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            load_more = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.woocommerce-load-more"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
            time.sleep(2)
            load_more.click()
            time.sleep(2)
        except:
            break

    links = get_all_product_links(driver)

    products = []
    for link in links:
        try:
            product = parse_product_page(driver, link)
            products.append(product)
            print(f"Parsed: {product.title}")
        except Exception as e:
            print(f"Error parsing {link}: {e}")

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in products], f, ensure_ascii=False, indent=4)

    driver.quit()

if __name__ == "__main__":
    main()