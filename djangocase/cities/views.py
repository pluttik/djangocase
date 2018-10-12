from django.shortcuts import render
from django.http import HttpResponse

import requests, csv, os

from .models import City, Hotel


djangocase_password = os.environ["DJANGOCASE_PASSWORD"]

requests_hotel = requests.get('http://rachel.maykinmedia.nl/djangocase/hotel.csv', auth=('python-demo', djangocase_password))
requests_city = requests.get('http://rachel.maykinmedia.nl/djangocase/city.csv', auth=('python-demo', djangocase_password))

decoded_content_hotel = requests_hotel.content.decode('utf-8')
reader_hotel = csv.reader(decoded_content_hotel.splitlines(), delimiter=';')
hotel_data = list(reader_hotel)

decoded_content_city = requests_city.content.decode('utf-8')
reader_city = csv.reader(decoded_content_city.splitlines(), delimiter=';')
cities_data = list(reader_city)


# below is part of the data. This can be used in case the http connection doesn't work, otherwise comment it out
#cities_data = [['AMS', 'Amsterdam'], ['ANT', 'Antwerpen'], ['ATH', 'Athene'], ['BAK', 'Bangkok'], ['BAR', 'Barcelona'], ['BER', 'Berlijn']]
#hotel_data = [['AMS', 'AMS01', 'Ibis Amsterdam Airport'], ['AMS', 'AMS02', 'Novotel Amsterdam Airport'], ['ANT', 'ANT01', 'Express by Holiday Inn'], ['ANT', 'ANT02', 'Eden'], ['ANT', 'ANT04', 'Astoria']]


# index view showing a list of all cities
def index(request):
    for city in cities_data:
        # check if the city coming in via the data is not already in the database
        check = City.objects.filter(city_abbreviation = city[0])
        # if not yet in the database, add it
        if len(check) == 0:
            new_city = City()
            new_city.city_abbreviation = city[0]
            new_city.city_name = city[1]
            new_city.save()
    cities = City.objects.all()
    if len(cities) == 0:
        return HttpResponse("No cities are available.")
    else:
        return render(request, 'cities/index.html', {'cities': cities})
    
    
# city view showing all hotels for a city
def city(request, city_id):
    # try and see if the city in the url exists
    try:
        my_city = City.objects.get(pk = city_id)
        # add new hotel data to database
        for hotel in hotel_data:
            # only attempt to add a hotel to database if it is situated in the city that was selected
            if my_city.city_abbreviation == hotel[0]: 
                # check if the hotel exists in the city already
                check = my_city.hotel_set.filter(hotel_code = hotel[1], hotel_name = hotel[2])
                # if it does not exist yet, add it to the database
                if len(check) == 0:
                    new_hotel = Hotel(hotel_city = hotel[0], hotel_code = hotel[1], hotel_name = hotel[2], city=my_city)
                    new_hotel.save()
    except (KeyError, City.DoesNotExist):
        return HttpResponse("That city does not exist.")
    return render(request, 'cities/city.html', {'city': my_city})  