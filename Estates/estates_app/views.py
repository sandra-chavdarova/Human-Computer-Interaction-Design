import random

from django.shortcuts import render, redirect

from .forms import EstateForm
from .models import *
from random import randint


# Create your views here.

def index(request):
    estates = Estate.objects.filter(is_sold=True, area__gt=100)
    context = {"estates": estates}
    return render(request, 'index.html', context)


def edit(request, id):
    estate = Estate.objects.filter(id=id).first()
    if request.method == "POST":
        form = EstateForm(request.POST, request.FILES, instance=estate)
        if form.is_valid():
            estate = form.save()
            EstateCharacteristic.objects.filter(estate=estate).delete()

            characteristics = [c.strip() for c in estate.characteristics.split(",")]
            for char in characteristics:
                char_obj = Characteristic.objects.filter(name=char).first()
                if not char_obj:
                    char_obj = Characteristic.objects.create(name=char, value=random.randint(50, 500))
                EstateCharacteristic.objects.create(estate=estate, characteristic=char_obj)
            return redirect('index')
    else:
        form = EstateForm(instance=estate)

    context = {"estate": estate, "form": form}
    return render(request, 'edit.html', context)
