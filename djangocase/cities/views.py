from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the INDEX view")
    
def city(request, city_id):
    return HttpResponse("This is a CITY view")