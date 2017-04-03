import csv
import os

from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display


display = Display(visible=0, size=(800, 600))
display.start()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE_NAME = 'scraped_data.csv'

file_path = os.path.join(BASE_DIR, CSV_FILE_NAME)

# Delete the file if already present
try:
    os.remove(file_path)
except OSError:
    pass

driver = webdriver.Firefox()

driver.get("https://www.liveyoursport.com/tennis/")

content = driver.page_source
content_str = content.encode('utf-8')

soup = BeautifulSoup(content_str, 'html.parser')

product_details = soup.findAll("div", {"class": "ProductDetails"})

scraped_data_list = []

i = 0
total = len(product_details)

for detail in product_details:
    link = detail.find('a', href=True)['href']
    print 'Scraping URL: ', link
    print 'Remaining: ', total-i

    driver.get(link)

    inner_content = driver.page_source
    inner_content_str = inner_content.encode('utf-8')
    inner_soup = BeautifulSoup(inner_content_str, 'html.parser')

    product_main = inner_soup.find("div", {"class": "ProductMain"})
    name = product_main.find("h1").text
    price = inner_soup.find("em", {"class": "ProductPrice"}).text
    description = inner_soup.find("span", {"class": "prod-descr"}).text
    scraped_data_list.append((name, price, description, link))

    writer = csv.writer(open(file_path, 'a'), quoting=csv.QUOTE_ALL)

    if i == 0:
        writer.writerow(['Product Name', 'Price', 'Description', 'URL'])

    writer.writerow([name.encode('utf-8'), price.encode('utf-8'), description.encode('utf-8'), link])

    i += 1

    print '\n'

driver.close()
display.stop()
