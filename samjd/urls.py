from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.starting_page, name="home-starting-page")
]
