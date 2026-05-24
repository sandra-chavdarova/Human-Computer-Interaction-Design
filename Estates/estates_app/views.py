from django.shortcuts import render, redirect

from .forms import EstateForm
from .models import *


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
            form.save()
            return redirect('index')
    else:
        form = EstateForm(instance=estate)

    context = {"estate": estate, "form": form}
    return render(request, 'edit.html', context)
