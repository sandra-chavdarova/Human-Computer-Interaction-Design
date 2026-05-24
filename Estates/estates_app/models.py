from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Agent(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    linkedIn = models.URLField(max_length=500, blank=True)
    sales = models.IntegerField(default=0)
    email = models.EmailField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()

    def __str__(self):
        return self.name


class Estate(models.Model):
    name = models.CharField(max_length=200)
    location = models.TextField()
    area = models.FloatField()
    date = models.DateField()
    photo = models.ImageField(upload_to='estates')
    is_reserved = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    characteristics = models.CharField(max_length=200, null=True, blank=True)

    def total_price(self):
        total = EstateCharacteristic.objects.filter(estate=self).aggregate(total=models.Sum('characteristic__value'))[
            'total']
        return total or 0

    def __str__(self):
        return f"{self.name} - {self.area} m² - {self.location}"


class AgentEstate(models.Model):
    agent = models.ForeignKey(to=Agent, on_delete=models.CASCADE)
    estate = models.ForeignKey(to=Estate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.agent} - {self.estate}"


class EstateCharacteristic(models.Model):
    estate = models.ForeignKey(to=Estate, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(to=Characteristic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.estate} - {self.characteristic}"
