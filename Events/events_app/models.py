from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    poster = models.ImageField(upload_to='media')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_outside = models.BooleanField(default=False)
    bands = CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    year_formed = models.IntegerField()
    performances = models.IntegerField()

    def __str__(self):
        return self.name


class BandEvent(models.Model):
    band = models.ForeignKey(to=Band, on_delete=models.CASCADE)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.band} - {self.event}"
