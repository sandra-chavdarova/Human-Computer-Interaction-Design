from django.db.models.fields import return_None
from django.shortcuts import render, redirect

from .forms import TripForm
from .models import Trip


# Create your views here.

def index(request):
    all_trips = Trip.objects.all()
    context = {"trips": all_trips, "pageTitle": "Our Trips"}
    return render(request, 'index.html', context)


def details(request, id):
    try:
        trip = Trip.objects.get(id=id)
    except Trip.DoesNotExist:
        return index(request)
    context = {"trip": trip}
    return render(request, "details.html", context)


def add(request):
    if request.method == "POST":
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('index')
    form = TripForm()
    return render(request, 'form.html', {"form": form})
