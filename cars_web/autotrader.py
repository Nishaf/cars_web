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
            'Save-Data': 'on',
            'referer': "https://www.autotrader.com",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
           }


def get_auto_trader_data(make, model, min_year, max_year):
    try:
        print('Retrieving Results....')
        url = 'https://www.autotrader.com/cars-for-sale/'
        url_changed = url + make + "/" + model + "/?startYear=" + min_year + "&endYear=" + max_year + "&numRecords=100"
        print(url_changed)
        data = requests.get("https://www.google.com")
        print(data.status_code)
        data = requests.get(url_changed, headers=headers, timeout=30)
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
        return 'Exception'











