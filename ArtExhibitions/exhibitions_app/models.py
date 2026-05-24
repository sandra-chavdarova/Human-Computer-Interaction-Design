from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Artist(models.Model):
    STYLES_CHOICES = [
        ("imp", "Impressionism"),
        ("pop", "Pop Art"),
        ("gra", "Graffiti")
    ]
    name = models.CharField(max_length=200)
    style = models.CharField(choices=STYLES_CHOICES, max_length=5)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Exhibition(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=200)

    def get_image(self):
        art = Art.objects.filter(exhibition=self).first()
        if art:
            return art.image
        return None

    def __str__(self):
        return self.title


class Art(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='arts')
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE)
    exhibition = models.ForeignKey(to=Exhibition, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
