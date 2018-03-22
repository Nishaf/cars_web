import os, sys, django
sys.path.append("/home/nishaf/PycharmProjects/Upwork_Projects")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

import requests
from bs4 import BeautifulSoup
from cars_web.models import CarsDetails
from cars_web.extra_functions import delete_previous_results, save_data


headers = {'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US;q=0.9,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Save-Data': 'on'
           }


def get_auto_trader_data(make, model, min_year, max_year):
    try:
        print('Retrieving Results....')
        url = 'https://www.autotrader.com/cars-for-sale/'
        url_changed = url + make + "/" + model + "/?startYear=" +min_year+ "&endYear=" + max_year + "&numRecords=100"
        print(url_changed)
        data = requests.get(url_changed, headers=headers, timeout=60)
        print(data.status_code)
        soup = BeautifulSoup(data.text)
        premium_listing = soup.find_all('div', attrs={'data-qaid': 'cntnr-lstng-premium'})
        listing = premium_listing + soup.find_all('div', attrs={'data-qaid': 'cntnr-lstng-featured'})
        if soup.find('strong', attrs={'class': 'text-xlg text-normal'}) is not None:
            print("No Data Found")
            return

        newly_listed, new_cars = [], []
        for i, j in enumerate(listing):
            new_var = j.find('p', attrs={'data-qaid': 'cntnr-newly-listed'})
            if new_var is not None:
                newly_listed.append(listing.pop(i))
                continue

        listing = newly_listed + listing
        if CarsDetails.objects.filter(website='autotrader.com', make=make, model=model).count() > 0:
            for i in listing:
                title_data = i.find('a', attrs={'class': 'text-md'})
                title = title_data.text.strip()
                link = "https://www.autotrader.com" + title_data.get('href')
                if not CarsDetails.objects.filter(make=make, model=model, link=link, title=title).exists():
                    new_cars.append((title, make, model, link))
        delete_previous_results('autotrader.com', make, model)
        for i in listing:
            title_data = i.find('a', attrs={'class': 'text-md'})
            title = title_data.text.strip()
            link = "https://www.autotrader.com" + title_data.get('href')
            save_data('autotrader.com', make, model, title, link)
        return new_cars

    except Exception as e:
        print(e)
        pass













def get_carsforsale_data(make, model, min_year, max_year):
    count = 0
    #delete_previous_results('carsforsale.com', make, model)
    # https://www.carsforsale.com/Search?Make=Toyota&Model=Camry&MinModelYear=2009&MaxModelYear=2012&PageNumber=4&
    # OrderBy=Relevance&OrderDirection=Desc
    url1 = 'https://www.carsforsale.com/Search?Make=' + str(make) + '&Model=' + str(model) + '&MinModelYear=' + str(min_year)\
           + '&MaxModelYear=' + str(max_year) + '&ZipCode=&Radius=100&PageNumber=%s&OrderBy=Relevance&OrderDirection=Desc'

    print(url1)
    print('Loading Data....')
    for i in range(1,5):
        url = url1 % (str(i))
        data = requests.get(url, headers=headers, timeout=60)
        soup = BeautifulSoup(data.text)
        listing = soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'})

    for item in listing:
        title = item.find('h4', attrs={'itemprop': 'name'}).text.strip()
        link = "https://www.carsforsale.com/" + (item.find('a', attrs={'class': 'vehicle-name vehicle-details-navigate'})).get('href')
        save_data('carsforsale.com', make, model,title, link)
        print("Title: " + title)
        print("Link: https://www.carsforsale.com/" + link)
        print("====================")


#get_carsforsale_data('Toyota','Camry', '2012', '12015')
#get_cars_data(33583, 55767)
#get_auto_trader_data()
#get_cars_data()

'''
url = "https://www.autotrader.com"
PROXY = '51.15.35.239:3128'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome('/home/nishaf/chromedriver', chrome_options=chrome_options)
driver.get(url)
#data = requests.get(url, headers=headers, proxies=proxy)
try:
    dialog = driver.find_element_by_xpath("//body[@class='modal-open']")
    dialog.send_keys(Keys.ESCAPE)
    sleep(1)
except:
    pass
make = driver.find_element_by_xpath("//select[@name='makeCodeListPlaceHolder']")
make.click()
for i in make.find_elements_by_xpath("//option"):
    if str(i.text).lower() == 'acura':
        i.click()

sleep(0.5)
make = driver.find_element_by_xpath("//select[@name='modelCodeListPlaceHolder']")
make.click()
for i in make.find_elements_by_xpath("//option"):
    if str(i.text).lower() == 'integra':
        i.click()

sleep(0.5)
driver.find_element_by_xpath("//input[@name='zip']").send_keys("99524")
sleep(10)
driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
sleep(10)
'''




