from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

# Scrapes the tesco's deal page and saves the products in an ordered spreadsheet!
# Idea inspired by https://github.com/duplaja/shipt-sales-to-csv
# Scraping is done with selenium and sifting of the page source is done with beautiful soup

################## Fetch the Data
print("Fetching page data")
driver = webdriver.Chrome()

# First find out how many items are on offer
driver.get("https://www.tesco.com/groceries/en-GB/promotions/alloffers?page=1&count=100")

# Wait untill the number of items on sale is displayed
wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located(By.CLASS_NAME, "pagination__items-displayed"))
print(driver.find_element_by_class_name("pagination__items-displayed"))



'''
################## Process the data into BeautifulSoup
# Load the data into BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')
print("Raw page data loaded")

# Manipulate the Data
listContainer = soup.find("ul", {"class": "product-list"})
rawItemList = listContainer.find_all("li")
'''
