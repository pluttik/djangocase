from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

from .models import City, Hotel


def create_city(city_abbreviation, city_name):
    # create a test city with abbreviation and name
    return City.objects.create(city_abbreviation=city_abbreviation, city_name=city_name)
    
    
class CityModelTests(TestCase):
    def test_city_model_string_representation(self):
        test_city = create_city(city_abbreviation='TST', city_name='Testcity')
        self.assertEqual(str(test_city), test_city.city_name)
        
    
class HotelModelTests(TestCase):
    def test_hotel_model_string_representation(self):
        test_city = create_city(city_abbreviation='TST', city_name='Testcity')
        test_hotel = test_city.hotel_set.create(hotel_name = 'Testhotel')
        self.assertEqual(str(test_hotel), test_hotel.hotel_name)
        
        
class CitiesIndexViewTests(TestCase):
    def test_city_view(self):
        # test city view
        url = reverse('cities:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CitiesCityViewTests(TestCase):
    def test_no_hotels_for_a_city(self):
        # test that a newly created city has no hotels
        test_city = create_city(city_abbreviation='TST', city_name='Testcity')
        url = reverse('cities:city', args=(test_city.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(Hotel.objects.all()), [])
        
    def test_new_city_exists_city_view(self):
        #test that a newly created city appears in the city view
        test_city = create_city(city_abbreviation='TST', city_name='Testcity')
        url = reverse('cities:city', args=(test_city.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_city.city_name)
        
    def test_city_does_not_exist(self):
        #test that a non-existing city gives the appropriate error message in city view
        test_city = create_city(city_abbreviation='TST', city_name='Testcity')
        url = reverse('cities:city', args=(test_city.id + 1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "That city does not exist.")