'''
- scraps dynamicly created contend on the web site using selenium
- checks number of pages and goes through them
- saves output to csv files; a file per page with job offers
- has a handlare that skips offers without detais that crash the code
- saves data in the PostgreSQL table
- Warszawa Key words
'''
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

import psycopg2


conn = psycopg2.connect( host="localhost", database="pracuj_pl", user="python_user", password="1234")
# create a cursor
cur = conn.cursor()




# webpage URL and searching options
city = 'warszawa'
key_word = 'data'

url = f'https://www.pracuj.pl/praca/{city};wp?rd=30'


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


## SCRAPPING 
soup = BeautifulSoup(driver.page_source, 'html.parser')

# selecting number of offers 
# nuber_offers = soup.find_all("span", class_="results-header__offer-count-text-number")[0].text
nuber_offers = soup.find_all("span", class_="results-header-listing__offer-count-text-number")[0].text

print()
print('Number of total results: ', nuber_offers)
print()
 # pagination
paginations = soup.find_all("li", class_="pagination_element-page")
print('Paginations: ',paginations[-1].text)
pages = int(paginations[-1].text)
print()

for page_number in range(1, pages + 1):
    
    print('\nGetting data from page no: ', page_number)

    # soups of paginated pages
    sub_page = url + '&pn=' + str(page_number)
    driver.get(sub_page)
    print(f"Opens website: {sub_page}")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    print("Driver is scrolling down the page...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    # selecting offers from a page
    results = soup.find_all("div", class_= "results")[0]
    offers_page = results.find_all("div", {"class": ["offer", "offer--border"]}) # we provide {"class"} when selector contains multiple classes

    # list that will hold scrapped data and it is used for a dataframe creation
    data = []

    for index, values in enumerate(offers_page):
        # handler had to be added for offers without details that were crashing the code
        try:
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

                # Writing data to the DATA_BASE
            col_names =  list(offer.keys())
            col_names_db = [col_name.replace("-", "_") for col_name in col_names]

            # prepering scrapped data for insterting to the DB
            row = [offer_url, position_name, company_name, company_location] + info_text
            row = [ str(i).strip().replace("'", '`') for i in row]

            base = ""
            for i,v in enumerate(col_names_db):
                base = base + " " + str(v) + "='" + str(row[i]) + "'"
                if i + 1 != len(col_names_db):
                    base += " AND"

            SQL = f"""INSERT INTO data_warsaw_all ({' ,'.join(col_names_db)})
                SELECT {" ,".join([ "'" + str(v) + "'" for v in row])}
                WHERE NOT EXISTS (SELECT 1 FROM data_warsaw WHERE {base});"""

            # insert data with cursor
            cur.execute(SQL)
            # commit the changes
            conn.commit()



        except:
            pass


    df = pd.DataFrame(data)
    df.drop_duplicates()
    df.to_csv(f'page_{page_number}.csv', encoding='utf-8', index=False)


# close the driver
driver.quit()

# close cursor
cur.close()

# close conection
conn.close()

print('Done')