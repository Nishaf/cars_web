from django.db import models


class CarsDetails(models.Model):
    website = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)



class CarModels(models.Model):
    website = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)

