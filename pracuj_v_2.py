'''
- scraps dynamically created contend on the web site using selenium


'''

import time

from string import printable
import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver

# webpage URL
city = 'warszawa'
radius = '40' # km 
key_word = 'data'

url = f'https://www.pracuj.pl/praca/{key_word};kw/{city};wp?rd=30'


# chrome driver
PATH = 'C:\Program Files (x86)\chromedriver.exe'

# chrom driver configuration
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless') # without opening browser

driver = webdriver.Chrome(PATH, options=options)

# open website using webdriver
driver.get(url)
print(f"Opens website: {url}")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
print("Driver is scrolling down the page...")

# waiting x secunds to fully load page e.g. 30
time.sleep(2)

## SCRAPPING 
soup = BeautifulSoup(driver.page_source, 'html.parser')

# selecting number of offers 
nuber_offers = soup.find_all("span", class_="results-header__offer-count-text-number")[0].text

print()
print('Number of total results: ', nuber_offers)
print()

# selecting offers from a page
results = soup.find_all("div", class_= "results")[0]
offers_page = results.find_all("div", {"class": ["offer", "offer--border"]}) # we provide {"class"} when selector contains multiple classes

# position URL
offer_url = offers_page[0].find_all("a", class_= "offer__click-area")   
print(offer_url[0]['href'])


# position NAME
position_name = offers_page[0].find_all("h2", class_="offer-details__title")[0].text
print('\n', position_name)

# company NAME
company_name = offers_page[0].find_all("span", class_="offer-company__wrapper")[0].text
print('\n', company_name)

# location
company_location = offers_page[0].find_all("li", class_="offer-labels__item offer-labels__item--location")[0].text
print('\n', company_location)

# more info
ul = offers_page[0].find_all('ul')[1]

info_names = [item['data-test'].replace("list-item-offer-", "") for item in ul.find_all('li', attrs={'data-test' : True})]
info_text = [item.text for item in ul.find_all('li')]

more_info = dict(zip(info_names, info_text))

print(more_info)



# close the driver
driver.quit()


# need to find the way to get the pagination number
# scrap only the data from results div