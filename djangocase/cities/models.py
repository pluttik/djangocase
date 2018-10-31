from django.db import models

class City(models.Model):
    """City model class."""
    city_abbreviation = models.CharField("Abbreviation for the city", max_length=50)
    city_name = models.CharField("Name of the city", max_length=400)
    def __str__(self):
        return self.city_name
    
class Hotel(models.Model):
    """Hotel model class."""
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    hotel_city = models.CharField("This hotel's city", max_length=50)
    hotel_code = models.CharField("The hotel's code", max_length=50)
    hotel_name = models.CharField("Name of the hotel", max_length=400)
    def __str__(self):
        return self.hotel_name
