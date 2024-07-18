from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_cities/", views.get_cities, name="get_cities"),
    path("api/city-stats/", views.city_stats, name="city_stats"),
]
