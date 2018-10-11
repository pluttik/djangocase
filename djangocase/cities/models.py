from django.db import models

class City(models.Model):
    city_abbreviation = models.CharField(max_length=50)
    city_name = models.CharField(max_length=400)
    
class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_city = models.CharField(max_length=50)
    hotel_code = models.CharField(max_length=50)
    hotel_name = models.CharField(max_length=400)
