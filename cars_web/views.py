from django.shortcuts import render
from django.views.generic import View
from .models import CarsDetails, CarModels
from django.http import JsonResponse
import re
from .autotrader import get_auto_trader_data, get_carsforsale_data, send_email
from .global_variables import auto_trader_years_list
import threading

class Homepage(View):
    def get(self, request):
        cars = CarModels.objects.all()
        cars_list = set()
        duplicate_list = []
        for car in cars:
            cars_list.add((car.website,car.make))

        cars_list = sorted(list(cars_list), key=lambda tup: tup[1])
        return render(request, 'homepage.html', {'cars': cars_list})



class GetModels(View):
    def get(self, request):
        make = request.GET['make']
        website = request.GET['website']
        models = list(CarModels.objects.filter(make=make, website=website).all().values())
        print(len(models))
        return JsonResponse({'res': 'success', 'models':models, 'years': auto_trader_years_list})


class RetrieveAutoTraderResults(View):
    lock = threading.Lock()
    def get_results(self, request):
        min_year = request.GET['min_year']
        max_year = request.GET['max_year']
        make = request.GET['make']
        model = request.GET['model']
        model = re.sub('\W+ ', '', model)
        model = re.sub("[\(\[].*?[\)\]]", "", model)
        new_cars = get_auto_trader_data(make, model, min_year, max_year)
        return make, model, new_cars

    def get(self, request):
        website = request.GET['website']
        print(website)
        if website == 'autotrader.com':
            print('here')
            self.lock.acquire()
            print("Working")
            make, model, new_cars = self.get_results(request)
            cars_data = list(CarsDetails.objects.filter(website='autotrader.com', make=make,model=model).all()
                             .values())
            self.lock.release()
            if cars_data is not None and len(cars_data) != 0:
                print("Length: " + str(len(new_cars)))
                if len(new_cars) != 0:
                    email = request.GET.get('email')
                    print(email)
                    if email:
                        print(email)
                        send_email(new_cars, email)
                return JsonResponse({'res': 'success', 'cars_details': cars_data})
            else:
                return JsonResponse({'res': 'error'})

        elif website == 'carsforsale.com':
            make, model, years = request.GET['make'], request.GET['model'], request.GET['year']
            print(make, model, years)
            get_carsforsale_data(make, model, years)
            cars_data = list(CarsDetails.objects.filter(website='carsforsale.com', make=make, model=model).all().values())
            print(len(cars_data))
            if len(cars_data) != 0:
                return JsonResponse({'res': 'success', 'cars_details': cars_data})
            else:
                return JsonResponse({'res':'error'})

