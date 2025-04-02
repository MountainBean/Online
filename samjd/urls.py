from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.starting_page, name="home-starting-page"),
    path("projects", views.projects_page, name="projects-page"),
    path("projects/<slug:slug>", views.project_detail, name="project-detail-page"),
    path("certs", views.certs, name="certs-page"),
]
