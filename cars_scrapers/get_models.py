import os, sys,  django
from cars_web.settings import BASE_DIR

sys.path.append(BASE_DIR)  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from time import sleep
from cars_web.models import CarModels
from cars_web.settings import BASE_DIR


class PopulateSelectingDatabase:
    def __init__(self):
        display = Display(visible=0, size=(1500,800))
        display.start()
        self.driver = webdriver.Chrome(BASE_DIR + "/chromedriver")#, chrome_options=self.get_chrome_options())
        self.autotrader = 'https://www.autotrader.com/'
        self.carsdotcom = 'https://www.cars.com/'
        self.carsforsale = 'https://www.carsforsale.com'
        self.car_gurus = "https://www.cargurus.com"

    def get_chrome_options(self):
        PROXY = '144.217.213.234:1080'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        return chrome_options

    def save_in_db(self, make, model):
        for j in model:
            print("Model: " + j.text.strip())
            if CarModels.objects.filter(website='autotrader.com', make=make.text.strip(),
                                        model=j.text.strip()).count() > 0:
                sleep(0.2)
                continue
            else:
                CarModels(website='autotrader.com', make=make.text.strip(), model=j.text.strip()).save()
            print("Saved")

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
        for i in make.find_elements_by_xpath("//option")[:-1]:
            print("Make: " + i.text.strip())
            i.click()
            sleep(2)
            model = self.driver.find_elements_by_xpath("//select[@name='modelCodeListPlaceHolder']//option")
            print(len(model))
            try:
                self.save_in_db(i, model)
            except:
                print("Failed to get model list.. Retrying...")
                sleep(2)
                model = self.driver.find_elements_by_xpath("//select[@name='modelCodeListPlaceHolder']//option")
                print(len(model))
                self.save_in_db(i, model)

            sleep(2)
            make = self.driver.find_element_by_xpath("//select[@name='makeCodeListPlaceHolder']")
            make.click()

    def run_carsdotcom(self):
        self.driver.get(self.carsdotcom)
        print("URL LOADED....")
        make = self.driver.find_element_by_xpath("//select[@id='makeSelect']")
        make.click()
        sleep(3)
        for i in make.find_elements_by_xpath("//select[@id='makeSelect']//option"):
            model_list = []
            print("Make: " + i.text.strip() + " ===> " + i.get_attribute('value'))
            i.click()
            sleep(3)
            model = self.driver.find_elements_by_xpath("//select[@id='modelSelect']//option")
            for j in model:
                if CarModels.objects.filter(website='cars.com', make=i.text.strip(), model=j.text.strip(),
                                            make_value=i.get_attribute('value'),
                                            model_value=j.get_attribute('value')).exists():
                    print("Already Present")
                    continue
                else:
                    CarModels(website='cars.com', make=i.text.strip(), model=j.text.strip(),
                              make_value=i.get_attribute('value'), model_value=j.get_attribute('value')).save()
                    print("Saved")
            sleep(2)
            make = self.driver.find_element_by_xpath("//select[@id='makeSelect']")
            make.click()
            sleep(2)

    def run_cargurus(self):
        self.driver.get(self.car_gurus)
        print("URL LOADED....")
        make = self.driver.find_element_by_xpath("//select[@id='carPickerUsed_makerSelect']")
        make.click()
        sleep(2)
        print(len(make.find_elements_by_xpath("//select[@id='carPickerUsed_makerSelect']//optgroup[2]//option")))
        for i in make.find_elements_by_xpath("//select[@id='carPickerUsed_makerSelect']//optgroup[2]//option")[80:]:
            model_list = []
            print("Make: " + i.text.strip() + " ===> " + i.get_attribute('value'))
            i.click()
            sleep(2)
            model = self.driver.find_elements_by_xpath("//select[@id='carPickerUsed_modelSelect']//optgroup//option")
            if len(model) == 0:
                model = self.driver.find_elements_by_xpath("//select[@id='carPickerUsed_modelSelect']//option")
            for j in model:
                if CarModels.objects.filter(website='cargurus.com', make=i.text.strip(), model=j.text.strip(),
                                            make_value=i.get_attribute('value'),
                                            model_value=j.get_attribute('value')).exists():
                    print("Already Present")
                    continue
                else:
                    CarModels(website='cargurus.com', make=i.text.strip(), model=j.text.strip(),
                              make_value=i.get_attribute('value'), model_value=j.get_attribute('value')).save()
                    print(i.text, j.text)
                    print("Saved")
            sleep(2)
            make = self.driver.find_element_by_xpath("//select[@id='carPickerUsed_makerSelect']")
            make.click()
            sleep(2)

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
PopulateSelectingDatabase().run_cargurus()
