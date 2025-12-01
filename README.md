# Kitka-Sonya WooCommerce Scraper

This Python script scrapes all products from [Kitka-Sonya](https://kitka-sonya.com/shop/) and saves them to a JSON file. It also downloads product images locally.

## 🚀 Features

- Automatically loads all products using the **Load More** button.
- Parses the following product details:
  - Title (`title`)
  - Current price (`current_price`)
  - Old price (`old_price`)
  - Rating (`rating`)
  - Image URL (`image_link`)
  - Local image path (`image_path`)
  - Additional description (`description`)
- Downloads product images into the `images` folder.
- Saves all products to `products.json`.

## ⚙️ Installation

1. Clone the repository or download the script:

```bash
git clone <https://github.com/DenisPrudius/parse>
```

2. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

3. Make sure you have **ChromeDriver** installed for Selenium, matching your Chrome version, and added to your system PATH.

**`requirements.txt` content example:**

```
selenium
beautifulsoup4
requests
```

## 📓 Usage

Run the script:

```bash
  python parse.py
```

The script will:

1. Open a browser window.
2. Load all products by clicking the **Load More** button multiple times.
3. Parse each product page.
4. Save the data to `products.json`.
5. Download all product images to the `images` folder.

The browser will close automatically when done.



