import os, sys, django
sys.path.append("/home/nishaf/PycharmProjects/Upwork_Projects")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

import requests, random
from bs4 import BeautifulSoup
from cars_web.extra_functions import save_data, delete_previous_results
from cars_web.models import CarsDetails
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from cars_web.settings import BASE_DIR

'''headers1  = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'referer': url,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}'''
#p = "13.125.174.77:3128"
#p = "107.174.26.61:1080"
#p = "74.208.163.28:3128"
#p = "35.196.26.166:3128"
p = "65.181.112.70:2018"
proxy = {'https': p, 'http': p}


def get_carsforsale_data(make, model, min_year, max_year):
    try:
        url = "https://www.carsforsale.com/Search?Make=Toyota&Model=Camry&MinModelYear=2009&MaxModelYear=2012&PageNumber=%s&OrderBy=Relevance&OrderDirection=Desc"
        url1 = 'https://www.carsforsale.com/Search?Make=' + str(make) + '&Model=' + str(model) + '&MinModelYear=' + str(min_year)\
               + '&MaxModelYear=' + str(max_year) + '&ZipCode=&Radius=100&OrderBy=Relevance&OrderDirection=Desc'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': 'ASP.NET_SessionId=d2srbgzlskumqdl1h32hejpq; ProfileId=; AvatarUrl=; FirstName=; LastName=; '
                      'AnalyticsAuthString=app_jzfq9zbugfrafizj eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJEYXRlVmFsaWQiOiJ'
                      'cL0RhdGUoMTUyMzczMzEzNzkyNSlcLyIsIkNvbnRleHQiOnsiSWQiOjAsIkF2YXRhclVybCI6bnVsbCwiRmlyc3ROYW1lIjpu'
                      'dWxsLCJMYXN0TmFtZSI6bnVsbCwiRW1haWwiOm51bGwsIlR5cGUiOiJhbm9ueW1vdXMifSwiQXBwS2V5IjoiYXBwX2p6ZnE5e'
                      'mJ1Z2ZyYWZpemoiLCJBcGlLZXkiOiJhcGlfNno0c3N2bHRhMW8zYmc4MCIsIlRva2VuIjpudWxsLCJJZCI6MH0.ZSdOoGyIGs'
                      'EIfbTgb33Jk7wxIkc6to_Kl_msOgVpoEc;'
                      'S=billing-ui-v3=9CYSjKfeeRHN45YRuUmYm9YGbQIXkAPW:billing-ui-v3-efe=9CYSjKfeeRHN45YRuUmYm9YGbQIXkAPW;'
                      'Initials=; Email=; Phone=; _ga=GA1.2.1316674710.1508593741; _gid=GA1.2.1750638669.1508593741; '
                      '_dc_gtm_UA-2399010-1=1; __asc=3497fe5a15f3f31b0a51be9c13b; __auc=3497fe5a15f3f31b0a51be9c13b; '
                      'GuardianEndpoint=https://api.carsforsale.com; LoggedIn=False; CONSENT:YES+PK.en+20170723-09-0;'
                      'MenagerieExternalEndpoint=https://cdn-static-blob.carsforsale.com; '
                      'serverid=extweb204|WriYw|WriYl;HSID=A1XARiDoQOcxEIWF7;HSID=AbYkIXmjvlhEYduPp;'
                      'APISID=H_HzOrkub3cOoe6F/AsrTYG-7rrAC7GT6c;D_ZUID=667BCB5F-5C16-31E9-9FC6-98BB36DCC1A7;'
                      'D_ZID=44BC7D8D-BC20-35E9-93B5-0B19DDA16909;D_UID=CA9E8F2C-F9E1-3750-B55C-36F4547A5CB7;'
                      'cfsApplyFilters=false;LoggedIn=False;SSID=A1fWc2jwwlIE9YQKY;SSID=AXcUvfRnq_zV4aWl3;',
            'Host': 'www.carsforsale.com',
            'Referer': 'https://www.carsforsale.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
        }
        listing = []
        url = url1
        print(url)
        print('Loading Data....')
        # data = requests.get("https://google.com", proxies=proxy)
        # print(data.status_code)
        data = requests.get(url, headers=headers, timeout=60)
        soup = BeautifulSoup(data.text)
        if soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'}):
            listing += soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'})
        else:
            print("Again RObot Error!!!")

        new_cars = []
        if CarsDetails.objects.filter(website='carsforsale.com', make=make, model=model).count() > 0:
            for item in listing:
                title = item.find('h4', attrs={'itemprop': 'name'}).text.strip()
                link = "https://www.carsforsale.com/" + \
                       (item.find('a', attrs={'class': 'vehicle-name vehicle-details-navigate'})).get('href')
                if not CarsDetails.objects.filter(make=make, model=model, link=link, title=title).exists():
                    new_cars.append((title, make, model, link))
        delete_previous_results(website='carsforsale.com', make=make, model=model)
        for item in listing:
            title = item.find('h4', attrs={'itemprop': 'name'}).text.strip()
            link = "https://www.carsforsale.com/" + \
                   (item.find('a', attrs={'class': 'vehicle-name vehicle-details-navigate'})).get('href')
            save_data('carsforsale.com', make, model, title, link)
            print("Title: " + title)
            print("Link: https://www.carsforsale.com/" + link)
            print("====================")

        return new_cars

    except Exception as e:
        print(e)


def login(driver):
    driver.get("https://carsforsale.com")
    driver.find_element_by_xpath("//li[@class='signInBtn open']//a//button").click()
    driver.find_element_by_xpath("//li[@class='signInBtn open']//ul//li//a").click()
    driver.find_element_by_xpath("//input[@id='profileLoginEmailModal']").send_keys("bsef14a531@gmail.com")
    driver.find_element_by_xpath("//input[@id='profileLoginPasswordModal']").send_keys("nishaf123")
    driver.find_element_by_xpath("//input[@id='login-submit']").click()


def get_chrome_options():
    #p = 'https://admin123:admin123@8.29.123.111:27401'
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument('--proxy-server=%s' % p)
    #chrome_options.add_argument("javascript.enabled")
    chrome_options.add_argument("--no-sandbox")
    return chrome_options


def get_carsforsale_data1(make, model, min_year, max_year):
    try:
        url = 'https://www.carsforsale.com/Search?Make=' + str(make) + '&Model=' + str(model) + '&MinModelYear=' + str(
            min_year) \
               + '&MaxModelYear=' + str(
            max_year) + '&ZipCode=&Radius=100&OrderBy=Relevance&OrderDirection=Desc'

        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Chrome(BASE_DIR + "/chromedriver")#, chrome_options=get_chrome_options())
        driver.implicitly_wait(20)
        listing = []
        driver.get(url)
        print('Loading Data....')
        soup = BeautifulSoup(driver.page_source)
        listing += soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'})
        #if listing is None
        '''if soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'}):
            listing += soup.find_all('li',
                                     attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'})

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(random.randrange(5))
            driver.find_element_by_xpath("//button[@class='btn btn-primary btn-pagination-next']").click()
            sleep(random.randrange(5))

        else:
            print("Robot Error!!")'''

        new_cars = []
        if CarsDetails.objects.filter(website='carsforsale.com', make=make, model=model).count() > 0:
            for item in listing:
                title = item.find('h4', attrs={'itemprop': 'name'}).text.strip()
                link = "https://www.carsforsale.com/" + \
                       (item.find('a', attrs={'class': 'vehicle-name vehicle-details-navigate'})).get('href')
                if not CarsDetails.objects.filter(make=make, model=model, link=link, title=title).exists():
                    new_cars.append((title, make, model, link))
        delete_previous_results(website='carsforsale.com', make=make, model=model)
        for item in listing:
            title = item.find('h4', attrs={'itemprop': 'name'}).text.strip()
            link = "https://www.carsforsale.com/" + \
                   (item.find('a', attrs={'class': 'vehicle-name vehicle-details-navigate'})).get('href')
            save_data('carsforsale.com', make, model, title, link)
            print("Title: " + title)
            print("Link: https://www.carsforsale.com/" + link)
            print("====================")
        driver.close()
        return new_cars

    except Exception as e:
        print(e)
        driver.close()
        pass


while True:
    get_carsforsale_data('Toyota','Camry', '2012', '2015')
    sleep_timer = random.randrange(120, 240)
    print(sleep_timer)
    sleep(sleep_timer)
    print("waking up...")
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




