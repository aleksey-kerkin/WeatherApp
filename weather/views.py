import requests
from django.db import models
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from .models import City, SearchHistory


def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url).json()
    if response["results"]:
        latitude = response["results"][0]["latitude"]
        longitude = response["results"][0]["longitude"]
        return latitude, longitude
    return None, None


def index(request):
    last_city = request.session.get("last_city", None)
    if request.method == "POST":
        city_name = request.POST.get("city")
        if not city_name:
            return HttpResponseBadRequest("City name is required")

        city, created = City.objects.get_or_create(name=city_name)
        city.search_count += 1
        city.save()
        request.session["last_city"] = city_name

        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, city=city)

        latitude, longitude = get_coordinates(city_name)
        if latitude is None or longitude is None:
            return HttpResponseBadRequest("Could not find coordinates for the city")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
        weather_response = requests.get(weather_url).json()
        weather_data = {
            "city": city_name,
            "temperature": weather_response["hourly"]["temperature_2m"][0],
            "time": weather_response["hourly"]["time"][0],
        }
        return render(
            request,
            "weather/index.html",
            {"weather_data": weather_data, "last_city": last_city},
        )
    return render(request, "weather/index.html", {"last_city": last_city})


def get_cities(request):
    if request.method == "GET":
        term = request.GET.get("term", "")
        cities = City.objects.filter(name__icontains=term)[:10]
        results = [city.name for city in cities]
        return JsonResponse(results, safe=False)


def city_stats(request):
    stats = (
        City.objects.values("name")
        .annotate(search_count=models.Count("searchhistory"))
        .order_by("-search_count")
    )
    return JsonResponse(list(stats), safe=False)
