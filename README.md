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
git clone https://github.com/DenisPrudius/parse
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

## 📃 Sample Output

```json
[
    {
        "title": "Батарейки Kodak, Type D, лужні, комплект з 3 штук",
        "current_price": 325.0,
        "old_price": null,
        "rating": 5.0,
        "image_link": "https://sp-ao.shortpixel.ai/client/to_auto,q_glossy,ret_img/https://kitka-sonya.com/wp-content/uploads/2024/07/batarejky-1000x1250.png",
        "description": {
            "Фірма": "Kodak",
            "Тип": "Type D",
            "Вид": "Лужні",
            "Комплект": "Три штуки"
        },
        "image_path": "images/batarejky-1000x1250.png"
    },
    {
        "title": "Автоматична годівниця з Wi-Fi",
        "current_price": 2229.0,
        "old_price": 2329.0,
        "rating": 4.96,
        "image_link": "https://sp-ao.shortpixel.ai/client/to_auto,q_glossy,ret_img/https://kitka-sonya.com/wp-content/uploads/2024/07/wi-fi_godivnyczya_golovna-2-1000x1250.png",
        "description": {
            "Об‘єм резервуару для корму": "3,5 л",
            "Висота": "330 мм",
            "Ширина": "150 мм",
            "Довжина": "170 мм",
            "Вага": "1 кг",
            "Довжина USB кабелю": "150 см",
            "Батарейки для резервного живлення": "Три штуки типу D (не входять у комплект)",
            "Діаметр мисочки": "15 см",
            "Матеріал мисочки": "нержавійка",
            "Матеріал корпусу": "пластик",
            "Гарантія": "12 місяців"
        },
        "image_path": "images/wi-fi_godivnyczya_golovna-2-1000x1250.png"
    }
]
```



