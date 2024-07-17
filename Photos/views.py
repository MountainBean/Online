from datetime import date
from django.shortcuts import render

from .models import Photographer, Photo


def starting_page(request):
    uploaded_photos = Photo.objects.all().order_by("date")
    num_photos = uploaded_photos.count()
    return render(request, "photos/index.html", {
        "uploaded_photos": uploaded_photos,
        "total_number_of_uploaded_photos": num_photos
    })
