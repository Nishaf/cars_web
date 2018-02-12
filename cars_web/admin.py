from django.contrib import admin
from .models import *

class CarsDetailsAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')

class CarModelsAdmin(admin.ModelAdmin):
    list_display = ('website', 'make', 'model')


admin.site.register(CarsDetails, CarsDetailsAdmin)
admin.site.register(CarModels, CarModelsAdmin)