# In your models.py
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    search_count = models.IntegerField(default=0)
    latitude = models.FloatField(default=0.0)  # Add default value
    longitude = models.FloatField(default=0.0)  # Add default value

    def __str__(self):
        return self.name
