import os, sys, django
sys.path.append("/home/nishaf/PycharmProjects/Upwork_Projects")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

import datetime
from dateutil.relativedelta import relativedelta
from cars_web.models import CarsDetails, CarModels
from cars_web.settings import BASE_DIR
from selenium import webdriver
from time import sleep
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from cars_web.extra_functions import delete_previous_results, save_data, cars_years_list

def in_dictlist(pair, my_dictlist):
    for this in my_dictlist:
        if this[pair[0]] == pair[1]:
            return this['value']
    return None


def get_years(min_year, max_year):
    years_list = []
    min_date = datetime.datetime.strptime(min_year, '%Y')
    max_date = datetime.datetime.strptime(max_year, '%Y')
    if max_date>min_date:
        years_range = relativedelta(max_date, min_date).years
        for i in range(0, years_range + 1):
            date = min_date + datetime.timedelta(366 * i)
            year = in_dictlist(('year', str(date.year)), cars_years_list)
            if year:
                years_list.append(year)
    else:
        years_range = relativedelta(min_date, max_date).years
        for i in range(0, years_range + 1):
            date = max_date + datetime.timedelta(366 * i)
            year = in_dictlist(('year', str(date.year)), cars_years_list)
            if year:
                years_list.append(year.strip())

    return years_list


def get_cars_data(make, model, min_year, max_year):
    try:
        car = CarModels.objects.filter(website='cars.com', make=make, model=model).first()
        years = get_years(min_year, max_year)
        url1 = 'https://www.cars.com/for-sale/searchresults.action/?mdId=' + str(car.make_value) + '&mkId=' \
               + str(car.model_value) + '&page=1&perPage=100' \
               '&rd=99999&sort=listed-newest&zc=60606&searchSource=GN_REFINEMENT&showMore=true'
                                        #'&yrId=' + str(min_year) + '&yrId=' + str(max_year)
        for i in years:
            url1 += '&yrId=' + str(i)

        print(url1)
        print('Loading Data....')
        display = Display(visible=0, size=(800, 600))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(BASE_DIR + '/chromedriver', chrome_options=chrome_options)
        driver.implicitly_wait(20)
        driver.get(url1)
        #data = requests.get(url1, headers=headers1, timeout=60)
        soup = BeautifulSoup(driver.page_source)
        driver.close()
        listings_list = soup.find('div', attrs={'id': 'srp-listing-rows-container'})
        listing = listings_list.find_all('div', attrs={'class': 'shop-srp-listings__listing'})
        print(len(listing))
        new_cars = []
        if CarsDetails.objects.filter(website='cars.com', make=make, model=model).count() > 0:
            for item in listing:
                title_data = item.find('h2', attrs={'class': 'cui-delta listing-row__title'})
                title = title_data.text.strip()
                link = "https://www.cars.com/" + (item.find('a')).get('href')
                if not CarsDetails.objects.filter(make=make, model=model, link=link, title=title).exists():
                    new_cars.append((title, make, model, link))
        delete_previous_results(website='cars.com', make=make, model=model)
        for item in listing:
            title_data = item.find('h2', attrs={'class': 'cui-delta listing-row__title'})
            title = title_data.text.strip()
            link = "https://www.cars.com/" + (item.find('a')).get('href')
            save_data('cars.com', make, model, title, link)
            print("Title: " + title)
            print("Link: https://www.cars.com/" + link)
            print("====================")

        return new_cars
    except Exception as e:
        print(e)
        pass

#get_cars_data('Acura', 'RLX', '2014', '2018')

def get_cars_dot_com_years(request):
    display = Display(visible=0, size=(800, 600))
    display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(BASE_DIR + '/chromedriver', chrome_options=chrome_options)
    driver.implicitly_wait(30)
    print('Hello')
    make, model = (request.GET.get('make')).strip(), (request.GET.get('model')).strip()
    car = CarModels.objects.filter(website='cars.com', make=make, model=model).first()
    url1 = 'https://www.cars.com/for-sale/searchresults.action/?mkId=' + str(car.make_value) + '&mdId=' + \
           str(car.model_value) + '&page=1&perPage=100&rd=99999&searchSource=GN_REFINEMENT&showMore=true&' \
                                  'sort=listed-newest&zc=60606'
    print(url1)
    driver.get(url1)
    try:
        more_filters = driver.find_element_by_xpath("//div[@class='toggle-show-more-filter  show-more']"
                                                    "//span[@class='toggle-show-more']")
        more_filters.click()
    except:
        sleep(2)
        more_filters = driver.find_element_by_xpath("//div[@class='toggle-show-more-filter  show-more']"
                                                    "//span[@class='toggle-show-more']")
        driver.execute_script("arguments[0].click();", more_filters)

    sleep(3)
    soup = BeautifulSoup(driver.page_source)
    years = soup.find_all('select', attrs={'name': 'yrId'})[0]
    all_years = years.find_all('option')
    years_list = []
    for i in all_years:
        years_list.append({'year': i.text, 'value': i.get('value')})

    driver.close()
    return years_list
