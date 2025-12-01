import json
import time
from dataclasses import dataclass, fields, astuple, asdict
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

BASE_URL = "https://kitka-sonya.com/"
PARSE_URL = urljoin(BASE_URL, "shop")

@dataclass
class Product:
    title: str
    price: str
    rating: str
    price_with_discount: str

PRODUCT_FIELDS = [field.name for field in fields(Product)]

driver = webdriver.Chrome()
driver.get(PARSE_URL)

wait = WebDriverWait(driver, 8)

while True:
    try:
        load_more = wait.until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "button.woocommerce-load-more")
            )
        )
        try:
            load_more.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            driver.execute_script("arguments[0].click();", load_more)

        time.sleep(2)

    except TimeoutException:
        break


def get_products():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".products-content")
    return [parse_single_product(item) for item in items]


def parse_single_product(product: Tag) -> Product:
    rating_element = product.select_one(".rating strong")
    rating = rating_element.text.strip() if rating_element else None

    price_element = product.select_one(".price")
    old_price = price_element.select_one("del .woocommerce-Price-amount.amount")
    if old_price:
        price = " ".join(old_price.stripped_strings).replace("\xa0", " ")
    else:
        new_price = price_element.select_one(".woocommerce-Price-amount.amount")
        price = " ".join(new_price.stripped_strings).replace("\xa0", " ")

    discount = product.select_one(".screen-reader-text")
    if discount:
        discount_text = discount.text.strip()
        price_with_discount = discount_text.split(":")[-1].replace("\xa0", " ").strip()
    else:
        price_with_discount = None

    return Product(
        title=product.select_one(".product-title").text.strip(),
        price=price,
        rating=rating,
        price_with_discount=price_with_discount,
    )


def write_to_json(products):
    data = [asdict(product) for product in products]
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def main():
    products = get_products()
    write_to_json(products)
    print(f"Save {len(products)} products in results.json")

if __name__ == "__main__":
    main()
