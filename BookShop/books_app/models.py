from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    price = models.FloatField()
    image = models.ImageField(upload_to='books')

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book} - {self.author}"
