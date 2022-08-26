'''
- scraps dynamically created content on the website using selenium
- scraps only the first page
- saves the output to the CSV
- uses firefox driver
'''

import time

from string import printable
import requests
from bs4 import BeautifulSoup
import pandas as pd

import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# webpage URL
city = 'warszawa'
radius = '40' # km 
key_word = 'data'

url = f'https://www.pracuj.pl/praca/{key_word};kw/{city};wp?rd=30'


# Firefox driver
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0' # to get it follow instructions in the video: https://www.youtube.com/watch?v=kpONBQ3muLg

PATH = 'C:\Program Files (x86)\geckodriver.exe'

firefox_service = Service(PATH)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)

driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

# open website using webdriver
driver.get(url)
print(f"Opens website: {url}")

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

# list that will hold scrapped data and it is used for a dataframe creation
data = []

for index, values in enumerate(offers_page):
    offer = {}

    # position URL
    offer_url = offers_page[index].find_all("a", class_= "offer__click-area")[0]['href']   
    offer['offer_url'] = offer_url

    # position NAME
    position_name = offers_page[index].find_all("h2", class_="offer-details__title")[0].text
    offer['position_name'] = position_name

    # company NAME
    company_name = offers_page[index].find_all("span", class_="offer-company__wrapper")[0].text
    offer['company_name'] = company_name

    # location
    company_location = offers_page[index].find_all("li", class_="offer-labels__item offer-labels__item--location")[0].text
    offer['company_location'] = company_location

    # more info
    ul = offers_page[index].find_all('ul')[1]

    info_names = [item['data-test'].replace("list-item-offer-", "") for item in ul.find_all('li', attrs={'data-test' : True})]
    info_text = [item.text for item in ul.find_all('li')]

    more_info = dict(zip(info_names, info_text))
    # adding more info to the dictionary
    offer.update(more_info)

    data.append(offer)



df = pd.DataFrame(data)
df.drop_duplicates() # drop duplicates
df.to_csv('test.csv', encoding='utf-8', index=False)





 # pagination_element-page 

paginations = soup.find_all("li", class_="pagination_element-page")
print('Paginations: ',paginations[-1].text)



# close the driver
driver.quit()


# need to find the way to get the pagination number
