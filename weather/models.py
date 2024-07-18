from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} searched for {self.city.name} on {self.search_date}"
        )
