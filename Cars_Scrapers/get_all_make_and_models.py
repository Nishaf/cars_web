import os, sys, django
sys.path.append("/home/nishaf/PycharmProjects/Upwork_Projects")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from time import sleep
from cars_web.models import CarModels
class PopulateSelectingDatabase():
    def __init__(self):
        display = Display(visible=0, size=(1500,800))
        display.start()
        self.driver = webdriver.Chrome('/home/nishaf/chromedriver')#, chrome_options=self.get_chrome_options())
        self.autotrader = 'https://www.autotrader.com/'
        self.carsdotcom = 'https://www.cars.com/'
        self.carsforsale = 'https://www.carsforsale.com'

    def get_chrome_options(self):
        PROXY = '51.15.35.239:3128'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        return chrome_options

    def run_autotrader(self):
        self.driver.get(self.autotrader)
        print("URL LOADED....")
        try:
            dialog = self.driver.find_element_by_xpath("//body[@class='modal-open']")
            dialog.send_keys(Keys.ESCAPE)
            sleep(1)
        except:
            pass
        make = self.driver.find_element_by_xpath("//select[@name='makeCodeListPlaceHolder']")
        make.click()
        for i in make.find_elements_by_xpath("//option")[1:-1]:
            model_list = []
            print("Make: " + i.text.strip())
            i.click()
            sleep(2)
            model = self.driver.find_elements_by_xpath("//select[@name='modelCodeListPlaceHolder']/option")
            for j in model:
                print("Model: " + j.text.strip())
                if CarModels.objects.filter(website='autotrader.com', make=i.text.strip(), model=j.text.strip()).count() > 0:
                    continue
                else:
                    CarModels(website='autotrader.com', make=i.text.strip(), model=j.text.strip()).save()
                print("Saved")
            sleep(2)
            make = self.driver.find_element_by_xpath("//select[@name='makeCodeListPlaceHolder']")
            make.click()

    def run_carsdotcom(self):
        self.driver.get(self.carsdotcom)
        print("URL LOADED....")
        make = self.driver.find_element_by_xpath("//select[@name='mkId']")
        make.click()
        for i in make.find_elements_by_xpath("//option")[1:]:
            model_list = []
            print("Make: " + i.text.strip())
            i.click()
            sleep(2)
            model = self.driver.find_elements_by_xpath("//select[@name='mdId']/option")
            for j in model:
                print("Model: " + j.text.strip())
                #CarModels(website='autotrader.com', make=i.text.strip(), model=j.text.strip()).save()
                print("Saved")
            sleep(2)
            make = self.driver.find_element_by_xpath("//select[@name='mkId']")
            make.click()

    def run_carsforsale(self):
        while True:
            try:
                self.driver.get(self.carsforsale)
                print("URL LOADED....")
                make = self.driver.find_element_by_xpath("//select[@id='basic-mm-make']")
                make.click()
                print(len(make.find_elements_by_xpath("//select[@id='basic-mm-make']/option")))
                for i in make.find_elements_by_xpath("//select[@id='basic-mm-make']/option")[260:]:
                    if  i.get_attribute('value') == "":
                        make_name = 'All Makes'
                        print("Make: " + make_name)
                    else:
                        make_name = i.get_attribute('value')
                        print("Make: " + make_name)
                    i.click()
                    sleep(2)
                    model_list = self.driver.find_elements_by_xpath("//select[@id='basic-mm-model']/option")
                    print(len(model_list))
                    if len(model_list) > 0:
                        for j in model_list:
                            if j.get_attribute('value') == "":
                                model = 'All Models'
                                print("Model: " + model)
                            else:
                                model = j.get_attribute('value')
                                print("Model: " + model)
                            if CarModels.objects.filter(website='carsforsale.com', make=make_name, model=model).count() > 0:
                                print("Already Present")
                                continue
                            else:
                                CarModels(website='carsforsale.com', make=make_name, model=model).save()
                            print("Saved")
                            make = self.driver.find_element_by_xpath("//select[@id='basic-mm-make']")
                            make.click()
                        sleep(2)
                    else:
                        if CarModels.objects.filter(website='carsforsale.com', make=make_name, model='All Models').count() > 0:
                            print("Already Present")
                            continue
                        else:
                            CarModels(website='carsforsale.com', make=make_name, model='All Models').save()
                        make = self.driver.find_element_by_xpath("//select[@id='basic-mm-make']")
                        make.click()
                        sleep(2)
                print("Completed")
                break
            except Exception as e:
                print("Exception Occured")
                print(e)
                continue
#CarModels.objects.filter(website='carsforsale.com').all().delete()
PopulateSelectingDatabase().run_carsforsale()