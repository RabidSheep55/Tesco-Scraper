from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

# Scrapes the tesco's deal page and saves the products in an ordered spreadsheet!
# Idea inspired by https://github.com/duplaja/shipt-sales-to-csv

# Scraping is done with selenium and sifting of the page source is done with beautiful soup
# Turns out there's no need for authentification

# Fetch the Data
print("Fetchin page data")

# Load the data into BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')
print("Raw page data loaded")

# Manipulate the Data
listContainer = soup.find("ul", {"class": "product-list"})
rawItemList = listContainer.find_all("li")
