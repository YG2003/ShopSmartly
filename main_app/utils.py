import requests
from bs4 import BeautifulSoup
import lxml


def GetData(url, website):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accepted-Language": "en-GB, en-US; q = 0.9, en; q = 0.8",
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    if website == "Amazon":
        name = soup.select_one(selector="#productTitle").getText()
        name = name.strip()

        price = soup.select_one(selector=".a-price-whole").getText()
        price = price.replace(",", "")
        price = float(price)

    if website == "Flipkart":
        name = soup.select_one(selector=".B_NuCI").getText()
        name = name.strip()

        price = soup.select_one(selector="._30jeq3").getText()
        price = price[1:]
        price = price.replace(",", "")
        price = float(price)

    return name, price
