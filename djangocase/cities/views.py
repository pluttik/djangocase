from django.shortcuts import render
from django.http import HttpResponse

import requests, csv, os

from .models import City, Hotel


djangocase_password = os.environ["DJANGOCASE_PASSWORD"]

def get_data(source): #api or csv
    cities_data = []
    hotel_data=[]
    City.objects.all().delete()
    if source == 'api':
        requests_hotel = requests.get('http://rachel.maykinmedia.nl/djangocase/hotel.csv', auth=('python-demo', djangocase_password))
        requests_city = requests.get('http://rachel.maykinmedia.nl/djangocase/city.csv', auth=('python-demo', djangocase_password))

        decoded_content_hotel = requests_hotel.content.decode('utf-8')
        reader_hotel = csv.reader(decoded_content_hotel.splitlines(), delimiter=';')
        hotel_data = list(reader_hotel)

        decoded_content_city = requests_city.content.decode('utf-8')
        reader_city = csv.reader(decoded_content_city.splitlines(), delimiter=';')
        cities_data = list(reader_city)
    elif source == 'csv':
        with open('cities/data/city.csv') as csvfile:
            reader_city = csv.reader(csvfile, delimiter=';')
            cities_data = list(reader_city)
        csvfile.close()
        with open('cities/data/hotel.csv') as csvfile:
            reader_hotel = csv.reader(csvfile, delimiter=';')
            hotel_data = list(reader_hotel)
        csvfile.close()
        #cities_data = [['AMS', 'Amsterdam'], ['ANT', 'Antwerpen'], ['ATH', 'Athene'], ['BAK', 'Bangkok'], ['BAR', 'Barcelona'], ['BER', 'Berlijn']]
        #hotel_data = [['AMS', 'AMS01', 'Ibis Amsterdam Airport'], ['AMS', 'AMS02', 'Novotel Amsterdam Airport'], ['ANT', 'ANT01', 'Express by Holiday Inn'], ['ANT', 'ANT02', 'Eden'], ['ANT', 'ANT04', 'Astoria']]

    # add city data to database
    for city in cities_data:
        new_city = City()
        new_city.city_abbreviation = city[0]
        new_city.city_name = city[1]
        new_city.save()
        # add hotel data to database
        hotel_data_here = [item for item in hotel_data if item[0] == city[0]]
        for hotel in hotel_data_here:
            # check if the hotel exists in the city already
            # note that there are DUPLICATE hotel names, but they have unique hotel codes
            # check = my_city.hotel_set.filter(hotel_code = hotel[1], hotel_name = hotel[2])
            # swap the line above for the one below if you want NO DUPLICATES
            check = new_city.hotel_set.filter(hotel_name = hotel[2])
            # if it does not exist yet, add it to the database
            if len(check) == 0:
                new_hotel = Hotel(hotel_city = hotel[0], hotel_code = hotel[1], hotel_name = hotel[2], city=new_city)
                new_hotel.save()
    
                
# index view showing a list of all cities
def index(request):
    get_data('api')
    cities = City.objects.all()
    # show error message if no cities are in the database
    if len(cities) == 0:
        return HttpResponse("No cities are available.")
    else:
        return render(request, 'cities/index.html', {'cities': cities})
    
    
# city view showing all hotels for a city
def city(request, city_id):
    # try and see if the city in the url exists
    try:
        my_city = City.objects.get(pk = city_id)
    except (KeyError, City.DoesNotExist):
        return HttpResponse("That city does not exist.")
    return render(request, 'cities/city.html', {'city': my_city})  