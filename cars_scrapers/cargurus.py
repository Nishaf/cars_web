import os, sys, django
sys.path.append("/home/nishaf/PycharmProjects/Upwork_Projects")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

import requests
from bs4 import BeautifulSoup
from cars_web.extra_functions import save_data, delete_previous_results
from cars_web.models import CarsDetails
from pyvirtualdisplay import Display
from selenium import webdriver
from cars_web.settings import BASE_DIR
from cars_web.models import CarModels
from time import sleep

headers = {'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US;q=0.9,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/63.0.3239.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Save-Data': 'on',
           }

def car_gurus():
    url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?" \
          "sourceContext=carGurusHomePage_false_0&newSearchFromOverviewPage=true&inventorySearchWidgetType=AUTO&" \
          "entitySelectingHelper.selectedEntity=d36&entitySelectingHelper.selectedEntity2=c1063&zip=75209&distance=50&" \
          "searchChanged=true&modelChanged=true&filtersModified=true"
    # data = requests.get("https://www.cargurus.com/Cars/new/searchresults.action?sourceContext=homePageNewCarTab_false_0"
    #                    "&selectedEntity=d295&zip=")
    '''https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?
    sourceContext=homePageNewCarTab_false_0&newSearchFromOverviewPage=true&inventorySearchWidgetType=AUTO&
    entitySelectingHelper.selectedEntity=d292&entitySelectingHelper.selectedEntity2=&zip=&distance=50&searchChanged=true
    &modelChanged=true&filtersModified=true'''
    data = requests.get("https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?"
                        "sourceContext=carGurusHomePage_false_0&newSearchFromOverviewPage=true&"
                        "inventorySearchWidgetType=AUTO&entitySelectingHelper.selectedEntity=c1119&"
                        "entitySelectingHelper.selectedEntity2=c1091&zip=")

    # entitySelectingHelper.selectedEntity=c1096    Starting Year
    # entitySelectingHelper.selectedEntity2=c1063   Ending Year
    print(data.status_code)
    soup = BeautifulSoup(data.text)
    print(soup)


def get_all_listings(driver):
    all_listing = []
    soup = BeautifulSoup(driver.page_source)
    listings_list = soup.find('div', attrs={'id': 'listingsDiv'})
    listing = listings_list.find_all('div')
    for i in listing:
        if i.get('id') and 'listing' in i.get('id'):
            print(i.get('id'))
            all_listing.append({"listing": i, "listing_id": i.get('id').split("_")[1]})
    return all_listing


def get_cargurus_data(make, model, min_year, max_year):
    try:
        url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?" \
              "sourceContext=homePageNewCarTab_false_0&newSearchFromOverviewPage=true&inventorySearchWidgetType=AUTO&" \
              "entitySelectingHelper.selectedEntity=" + min_year + "&entitySelectingHelper.selectedEntity2=" + max_year\
              + "&zip=&distance="

        print(url)
        print('Loading Data....')
        display = Display(visible=0, size=(800, 600))
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(BASE_DIR + "/chromedriver_linux", chrome_options=chrome_options)
        driver.implicitly_wait(20)
        driver.get(url)
        print("Hello")
        all_listing = get_all_listings(driver)
        pages = 1
        while pages < 6:
            try:
                driver.find_element_by_xpath("//a[@class='nextPageElement js-go-to-next-page ']").click()
                sleep(1)
                all_listing += get_all_listings(driver)
                pages += 1
            except:
                break
        print(pages)
        driver.close()
        print(len(all_listing))
        new_cars = []
        if CarsDetails.objects.filter(website='cargurus.com', make=make, model=model).count() > 0:
            for item in all_listing:
                link = url + "#listing=" + item['listing_id']
                item = item['listing']
                title = item.find('h4', attrs={'class': 'cg-dealFinder-result-model'}).text.strip()
                if not CarsDetails.objects.filter(make=make, model=model, link=link, title=title).exists():
                    new_cars.append((title, make, model, link))
        delete_previous_results(website='cargurus.com', make=make, model=model)
        for item in all_listing:
            link = url + "#listing=" + item['listing_id']
            item = item['listing']
            title = item.find('h4', attrs={'class': 'cg-dealFinder-result-model'}).text.strip()
            save_data('cargurus.com', make, model, title, link)
            print("Title: " + title)
            print("Link: " + link)
            print("====================")

        return new_cars

    except Exception as e:
        print(e)
        try:
            driver.close()
            return "Exception"
        except:
            return "Exception"


def get_cargurus_dot_com_years(request):
    try:
        make, model = (request.GET.get('make')).strip(), (request.GET.get('model')).strip()
        car = CarModels.objects.filter(website='cargurus.com', make=make, model=model).first()
        url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?" \
            "sourceContext=homePageNewCarTab_false_0&newSearchFromOverviewPage=true&inventorySearchWidgetType=AUTO&"\
            "entitySelectingHelper.selectedEntity="+ car.model_value + "&zip=&distance="
        data = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(data.text)
        years = soup.find("select", attrs={'class': 'select car-select-dropdown btn-small form-control ft-year'})
        all_years = years.find_all('option')[1:]

        years_list = []
        for i in all_years:
            years_list.append({'year': i.text, 'value': i.get('value')})

        return years_list
    except Exception as e:
        print(e)
        return None




