from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:city_id>/city/', views.city, name='city'),
]