from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Guide(models.Model):
    name = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Travel(models.Model):
    place = models.CharField(max_length=200)
    price = models.FloatField()
    duration = models.IntegerField()
    image = models.ImageField(upload_to='destinations')
    guide = models.ForeignKey(to=Guide, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.place}"
