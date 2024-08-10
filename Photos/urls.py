from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("all_photos", views.all_photos, name="all-photos-page"),
    path("all_photos/<slug:slug>", views.photo_detail, name="photo-detail-page")
]
