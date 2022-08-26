'''
scraps only basic info that is not dynamicaly cretaed by javascript
'''


from string import printable
import requests
from bs4 import BeautifulSoup
import pandas as pd


'''
sample url for filtring positions by location AND a 'data' key word
    https://www.pracuj.pl/praca/data;kw/warszawa;wp?rd=30
'''
city = 'warszawa'
radius = '40' # km 
key_word = 'data'

url = f'https://www.pracuj.pl/praca/{key_word};kw/{city};wp?rd=30'


page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


# selecting number of offers 
nuber_offers = soup.find_all("span", class_="results-header__offer-count-text-number")[0].text


print()
print(nuber_offers)
print()
print(url)


# selecting offers from a page
offers_page = soup.find_all("div", {"class": ["offer", "offer--border"]}) # we provide {"class"} when selector contains multiple classes

print(len(offers_page))
print()
# position URL
offer_url = offers_page[0].find_all("a", class_= "offer__click-area")   
print(offer_url[0]['href'])

'''
# Initialize data to lists.
data = [{'a': 1, 'b': 2, 'c': 3},
        {'a': 10, 'b': 20, 'c': 30}]
  
# Creates DataFrame.
df = pd.DataFrame(data)
'''

data = []

# position NAME
position_name = offers_page[0].find_all("h2", class_="offer-details__title")[0].text
print('\n', position_name)

# company NAME
company_name = offers_page[0].find_all("span", class_="offer-company__wrapper")[0].text
print('\n', company_name)

# location
company_location = offers_page[0].find_all("li", class_="offer-labels__item offer-labels__item--location")[0].text
print('\n', company_location)
