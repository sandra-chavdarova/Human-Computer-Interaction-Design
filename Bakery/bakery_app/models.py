from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Baker(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Cake(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    weight = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='cakes')
    baker = models.ForeignKey(to=Baker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
