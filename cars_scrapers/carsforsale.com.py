from selenium import webdriver
import os
from bs4 import BeautifulSoup
from cars_web.settings import BASE_DIR
from cars_web.models import CarModels


def get_chrome_options():
    p = 'https://admin123:admin123@8.29.123.111:27401'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument('--proxy-server=%s' % p)
    chrome_options.add_argument("javascript.enabled")
    return chrome_options


def get_carsforsale_data(make, model, min_year, max_year):
    driver = webdriver.Chrome(BASE_DIR + '/chromedriver')#, chrome_options=get_chrome_options())
    url1 = 'https://www.carsforsale.com/Search?Make=' + str(make) + '&Model=' + str(model) + '&MinModelYear=' \
           + str(min_year) + '&MaxModelYear=' + str(max_year) + \
           '&ZipCode=&Radius=100&PageNumber=%s&OrderBy=Relevance&OrderDirection=Desc'

    print(url1)
    for i in range(1,5):
        url = url1 % (str(i))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        listing = soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'})

    driver.close()


get_carsforsale_data('Toyota', 'Camry', '2010', '2015')


