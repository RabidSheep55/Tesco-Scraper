'''
Scrapes the tesco's deal page and saves the products in an ordered spreadsheet!
Idea inspired by https://github.com/duplaja/shipt-sales-to-csv
Scraping is done with selenium and sifting of the page source is done with beautiful soup

NOTES:
    - More items are shown to be on sale when not logged in... why?

'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

from bs4 import BeautifulSoup

################## Fetch the Data
driver = webdriver.Chrome()

# First find out how many items are on offer
driver.get("https://www.tesco.com/groceries/en-GB/promotions/alloffers")

# Wait until the number of items on sale is displayed
wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__items-displayed")))
itemsOnSale = re.search(r"(?<=of )\d+", driver.find_element_by_class_name("pagination__items-displayed").text).group()
print("Total of", itemsOnSale, "items on sale right now")





'''
################## Process the data into BeautifulSoup
# Load the data into BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')
print("Raw page data loaded")

# Manipulate the Data
listContainer = soup.find("ul", {"class": "product-list"})
rawItemList = listContainer.find_all("li")
'''
