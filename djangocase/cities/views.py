from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command
from apscheduler.schedulers.background import BackgroundScheduler
from django.core import serializers

import requests, csv, os

from .models import City, Hotel


djangocase_password = os.environ["DJANGOCASE_PASSWORD"]


# the first two functions take care of daily database HTTP scheduling

def tick(input_type): #api or csv
    """Get the data from the designated source."""
    #get_data('csv')
    get_data(input_type)
    print('(Re-)loaded the data')

    
def start_job():
    """Time scheduler."""
    global job
    job = scheduler.add_job(lambda: tick(input_type), 'interval', hours=24)
    try:
        scheduler.start()
    except:
        pass

        
def get_data(source): #api or csv
    """Get the data, either via api or from csv files."""
    cities_data = []
    hotel_data=[]
    #City.objects.all().delete()
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
        with open('cities/data/hotel.csv') as csvfile:
            reader_hotel = csv.reader(csvfile, delimiter=';')
            hotel_data = list(reader_hotel)

    # add city data to database
    for city in cities_data:
        new_city, created = City.objects.get_or_create(city_name = city[1], city_abbreviation = city[0])
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
                new_hotel, created = Hotel.objects.get_or_create(hotel_city = hotel[0], hotel_code = hotel[1], hotel_name = hotel[2], city=new_city)
                new_hotel.save()
    
                
def index(request):
    """Index view showing a list of all cities."""
    cities = City.objects.all()
    # show error message if no cities are in the database
    if len(cities) == 0:
        return HttpResponse("No cities are available.")
    else:
        return render(request, 'cities/index.html', {'cities': cities})
    
    
def city(request, city_id):
    """City view showing all hotels for a city."""
    # try and see if the city in the url exists
    try:
        my_city = City.objects.get(pk = city_id)
    except (KeyError, City.DoesNotExist):
        return HttpResponse("That city does not exist.")
    return render(request, 'cities/city.html', {'city': my_city})  
    

def all_json_hotels(request, city_name):
    """All_json_hotels view for filling drop-down menu in index view."""
    current_city = City.objects.get(city_name = city_name)
    hotels = Hotel.objects.all().filter(city = current_city)
    json_hotels = serializers.serialize("json", hotels)
    return HttpResponse(json_hotels)
    
call_command('load_data')
scheduler = BackgroundScheduler()
job = None
start_job()