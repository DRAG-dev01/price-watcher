from bs4 import BeautifulSoup
import requests

response: requests.Response = requests.get("https://webscraper.io/test-sites/product/bmw-e24-635csi-1954-c002")
response.raise_for_status()

soup = BeautifulSoup(response.text, features="html.parser")

tag = soup.find(name="span", attrs={"data-price": True})

if tag is None:
    raise ValueError("Price not found.")

price = int(tag["data-price"])

print(price)
print(type(price))
