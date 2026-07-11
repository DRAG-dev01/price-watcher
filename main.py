import random
import time

import requests
import schedule
from bs4 import BeautifulSoup

from database import (
    add_product,
    create_table,
    get_products_by_url,
    update_price,
)
from notifier import send_discord_message

PRODUCT_URL = "https://webscraper.io/test-sites/product/bmw-e24-635csi-1954-c002"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
]

HEADERS = {"User-Agent": random.choice(USER_AGENTS)}


def scrape_product():
    """Scrape product information from the website."""

    response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h2", class_="title")
    price_tag = soup.find("span", attrs={"data-price": True})

    if title_tag is None:
        raise ValueError("Product title not found.")

    if price_tag is None:
        raise ValueError("Product price not found.")

    product_name = title_tag.text.strip()
    price = int(price_tag["data-price"])

    return product_name, price, PRODUCT_URL


def check_price():
    product_name, current_price, url = scrape_product()

    print("Product:", product_name)
    print("Current price:", current_price)

    stored_product = get_products_by_url(url)

    print("Database product:", stored_product)

    if stored_product is None:
        add_product(product_name, current_price, url)
        print("Added to database.")
        return

    old_price = stored_product[1]

    print("Old price:", old_price)

    if current_price < old_price:
        print("PRICE DROPPED - Sending Discord")

        send_discord_message(f"""
📉 **Price Drop Detected!**

**Product:** {product_name}

Old Price: ${old_price}
New Price: ${current_price}

{url}
""")

        update_price(url, current_price)

    elif current_price > old_price:
        print("Price increased")
        update_price(url, current_price)

    else:
        print("No change")


def main():
    create_table()

    try:
        check_price()
    except requests.RequestException as e:
        print(f"Network Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    schedule.every(1).hour.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
