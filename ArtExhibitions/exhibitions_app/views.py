from django.shortcuts import render, redirect

from .forms import ExhibitionForm
from .models import *


# Create your views here.

def index(request):
    exhibitions = Exhibition.objects.all()
    context = {"exhibitions": exhibitions}
    return render(request, 'index.html', context)


def add(request):
    if request.method == "POST":
        form = ExhibitionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = ExhibitionForm()
    return render(request, 'add.html', {"form": form})
