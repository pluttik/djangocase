from django.db import models

class City(models.Model):
    """City model class."""
    city_abbreviation = models.CharField(max_length=50)
    city_name = models.CharField(max_length=400)
    def __str__(self):
        return self.city_name
    
class Hotel(models.Model):
    """Hotel model class."""
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_city = models.CharField(max_length=50)
    hotel_code = models.CharField(max_length=50)
    hotel_name = models.CharField(max_length=400)
    def __str__(self):
        return self.hotel_name
