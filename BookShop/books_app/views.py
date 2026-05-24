from django.shortcuts import render, redirect

from .forms import BookForm
from .models import *


# Create your views here.

def index(request):
    books = Book.objects.all().distinct()
    authors = BookAuthor.objects.all()
    context = {"books": books, "authors": authors}
    return render(request, 'index.html', context)


def edit(request, id):
    book = Book.objects.filter(id=id).first()

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BookForm(instance=book)

    return render(request, 'edit.html', {"form": form, "book": book})
