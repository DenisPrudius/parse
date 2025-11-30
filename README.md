# 🐾 Product Parser – Kitka-Sonya Shop

Цей проєкт — парсер товарів із сайту [kitka-sonya.com](https://kitka-sonya.com/shop/),
Скрипт написаний на Python проходить каталог товарів, збирає інформацію з плиток та автоматично зберігає дані у json-файл.

---

## 📌 Функціонал

### 🔹 Парсинг товарів
Зі сторінок каталогу збирається така інформація:
- **Назва товару**
- **Ціна**
- **Ціна зі знижкою(якщо є)**
- **Рейтинг**

### 🔹 Автоматична пагінація
Скрипт переходить на наступні сторінки, доки не буде зібрано всі товари.

### 🔹 Збереження результатів
Усі дані записуються у файл: 
results.json

---

## ▶️ Запуск


```bash
python parse.py
```

# (EN)
# 🐾 Product Parser – Kitka-Sonya Shop

This project is a Python-based web scraper that collects product data from  
[kitka-sonya.com](https://kitka-sonya.com/shop/).  
The script iterates through all catalog pages, extracts product information, and saves the results into a json file.

---

## 📌 Features

### 🔹 Product Parsing
The script collects the following data from each product tile:
- **Product title**
- **Price**
- **Discounted price (if available)**
- **Rating**

### 🔹 Automatic Pagination
The scraper follows pagination links until all products are collected.

### 🔹 Data Export
All parsed data is saved into: 

results.json


---

## ▶️ How to Run

```bash
python parse.py
