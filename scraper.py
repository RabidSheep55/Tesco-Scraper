from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from prettytable import PrettyTable
import re
from bs4 import BeautifulSoup

'''
Scrapes the tesco's deal page and saves the products in an ordered spreadsheet!
Idea inspired by https://github.com/duplaja/shipt-sales-to-csv
Scraping is done with selenium and sifting of the page source is done with beautiful soup

NOTES:
    - More items are shown to be on sale when not logged in... why?
    - Why do they still display unavailable products? (53/7522)
'''

batchSize = 100 # max 1000; optimal around 100
headless = True

# Fetch the products
class Product:
    def __init__(self, name, link, offer, price):
        self.name = name
        self.link = link
        self.offer = offer
        self.price = price

    def processOffer(self):  # Turns the offer phrase into a percentage
        oldPrice = re.search(r"Was\s£?([\d|.]+p?)", self.offer)  # Regex captures the old price from the offer phrase
        if oldPrice:
            if "p" in oldPrice[1]:
                prev = float("0." + oldPrice[1][:-1])
            else:
                prev = float(oldPrice[1])
            self.reduction = round((prev - self.price)/prev, 3)
            self.multibuy = 1
        else:
            bunchDeal = re.search(r"(\d+)\sfor\s£?([\d|.]+p?)", self.offer)  # Extracts the multibuy offer details
            if bunchDeal:
                self.multibuy = int(bunchDeal[1])
                if "p" in bunchDeal[2]:
                    combinedPrice = float("0." + bunchDeal[2][:-1])
                else:
                    combinedPrice = float(bunchDeal[2])
                effectiveCost = self.multibuy * self.price
                self.reduction = round((effectiveCost - combinedPrice)/combinedPrice, 3)
            else:
                self.reduction = 0

        # print("Processed offer", self.offer, "into", self.reduction)

def fetcher():
    if headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome()

    # First find out how many items are on offer
    driver.get("https://www.tesco.com/groceries/en-GB/promotions/alloffers")

    # Wait until the number of items on sale is displayed
    wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__items-displayed")))
    itemsOnSale = int(re.search(r"(?<=of )\d+", driver.find_element_by_class_name("pagination__items-displayed").text).group())
    print("There is a total of", itemsOnSale, "items on sale right now")

    # Now fetch and extract their information by batches
    unavailable = 0
    # itemsOnSale = 100
    productList = []
    for i in range(1, int(itemsOnSale/batchSize) + 1):
        url = "https://www.tesco.com/groceries/en-GB/promotions/alloffers?page={}&count={}".format(str(i), str(batchSize))
        driver.get(url)
        wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination-component")))

        data = driver.find_element_by_css_selector("ul.product-list").get_attribute('innerHTML')
        soup = BeautifulSoup(data, 'html.parser')
        rawItemList = soup.find_all("li", recursive=False)

        for item in rawItemList:
            itemPrice = item.find("span", {"class": "value"})
            if itemPrice:  # Sometimes, unavailable products are still displayed, but without a price
                itemName = item.find("div", {"class": "product-details--content"}).find("a").text
                itemLink = "https://www.tesco.com/" + item.find("div", {"class": "product-details--content"}).find("a")['href']
                itemOffer = item.find("span", {"class": "offer-text"}).text
                itemPrice = item.find("span", {"class": "value"}).text
                productList += [Product(itemName, itemLink, itemOffer, float(itemPrice))]
            else:
                unavailable += 1

    print("There were", unavailable, "unavailable products")
    return productList

def sortkey(product):
    return product.reduction

if __name__ == '__main__':
    productList = fetcher()

    for product in productList:
        product.processOffer()

    sprods = sorted(productList, key=sortkey, reverse=True)

    table = PrettyTable(['Item Name', 'Price', 'Reduction', 'Multibuy'])
    for a in sprods:
        if a.reduction != 0:
            table.add_row([a.name, a.price, str(round(a.reduction*100, 1)) + "%", a.multibuy])

    print(table)
