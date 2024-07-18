from django.test import Client, TestCase
from django.urls import reverse

from .models import City


class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(name="London", search_count=0)

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "weather/index.html")

    def test_city_search(self):
        response = self.client.post(reverse("index"), {"city": "London"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "London")
