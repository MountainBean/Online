from datetime import date
from django.shortcuts import render, get_object_or_404


def starting_page(request):
    return render(request, "samjd/index.html")
