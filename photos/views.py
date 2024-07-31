from datetime import date
from django.shortcuts import render, get_object_or_404

from .models import Photographer, Photo


def starting_page(request):
    latest_photos = Photo.objects.all().order_by("-date")[:3]
    return render(request, "photos/index.html", {
        "latest_photos": latest_photos
    })


def all_photos(request):
    all_photos = Photo.objects.all().order_by("-date")
    return render(request, "photos/all-photos.html", {
        "all_photos": all_photos
    })


def photo_detail(request, slug):
    target_photo = get_object_or_404(Photo, slug=slug)
    return render(request, "photos/photo-detail.html", {
        "photo": target_photo
    })
