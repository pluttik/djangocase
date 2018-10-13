from django.contrib import admin
from .models import City, Hotel

class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 3

class CityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['city_abbreviation']}),
        ('City name', {'fields': ['city_name']}),
        ]
    inlines = [HotelInline]
    list_display = ('city_abbreviation', 'city_name')
    search_fields = ['city_name']

admin.site.register(City, CityAdmin)