from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Trip(models.Model):
    place = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.place}"


class Guide(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"


class TripGuide(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trip} - {self.guide}"
