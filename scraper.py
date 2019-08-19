from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
from time import time

'''
Scrapes the tesco's deal page and saves the products in an ordered spreadsheet!
Idea inspired by https://github.com/duplaja/shipt-sales-to-csv
Scraping is done with selenium and sifting of the page source is done with beautiful soup

NOTES:
    - More items are shown to be on sale when not logged in... why?

'''

batchSize = 100 # max 1000

################## Fetch the Data
driver = webdriver.Chrome()

# First find out how many items are on offer
driver.get("https://www.tesco.com/groceries/en-GB/promotions/alloffers")

# Wait until the number of items on sale is displayed
wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__items-displayed")))
itemsOnSale = int(re.search(r"(?<=of )\d+", driver.find_element_by_class_name("pagination__items-displayed").text).group())
print("There is a total of", itemsOnSale, "items on sale right now")

# Now fetch all of them by batches
itemsOnSale = 1000
start = time()
products = []
for i in range(1, int(itemsOnSale/batchSize) + 1):
    url = "https://www.tesco.com/groceries/en-GB/promotions/alloffers?page={}&count={}".format(str(i), str(batchSize))
    driver.get(url)
    wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination-component")))

    data = driver.find_element_by_css_selector("ul.product-list").get_attribute('innerHTML')
    soup = BeautifulSoup(data, 'html.parser')
    rawItemList = soup.find_all("li", recursive=False)

    for item in rawItemList:
        itemName = item.find("div", {"class": "product-details--content"}).find("a").text
        products += [{"name": itemName}]

end = time()
print("Fetched items in", end-start, "ms")
print(len(products))

'''
################## Process the data into BeautifulSoup
# Load the data into BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')
print("Raw page data loaded")

# Manipulate the Data
listContainer = soup.find("ul", {"class": "product-list"})
rawItemList = listContainer.find_all("li")
'''
