import requests
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from .models import City


def get_coordinates(city_name):
    # Use a geocoding service to get latitude and longitude
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(geocoding_url).json()
    if response["results"]:
        latitude = response["results"][0]["latitude"]
        longitude = response["results"][0]["longitude"]
        return latitude, longitude
    return None, None


def index(request):
    if request.method == "POST":
        city_name = request.POST.get("city")
        if not city_name:
            return HttpResponseBadRequest("City name is required")

        city, created = City.objects.get_or_create(name=city_name)
        if created:
            latitude, longitude = get_coordinates(city_name)
            if latitude is None or longitude is None:
                return HttpResponseBadRequest("Could not find coordinates for the city")
            city.latitude = latitude
            city.longitude = longitude
            city.save()

        city.search_count += 1
        city.save()

        url = f"https://api.open-meteo.com/v1/forecast?latitude={city.latitude}&longitude={city.longitude}&hourly=temperature_2m"
        response = requests.get(url).json()
        weather_data = {
            "city": city_name,
            "temperature": response["hourly"]["temperature_2m"][0],
            "time": response["hourly"]["time"][0],
        }
        return render(request, "weather/index.html", {"weather_data": weather_data})
    return render(request, "weather/index.html")
