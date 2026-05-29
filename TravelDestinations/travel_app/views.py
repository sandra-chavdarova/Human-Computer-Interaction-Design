from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.

def index(request):
    destinations = Travel.objects.all()
    context = {"destinations": destinations}
    return render(request, 'index.html', context)


def add(request):
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            guide = Guide.objects.filter(user=request.user).first()
            destination.guide = guide
            destination.save()
            return redirect('index')
    form = DestinationForm()
    context = {"form": form}
    return render(request, 'add.html', context)
