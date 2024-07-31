from django.db import models
from django.urls import reverse


class Photographer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name()


class Photo(models.Model):
    title = models.CharField(max_length=256)
    location = models.CharField(max_length=80)
    image = models.ImageField(upload_to="images", null=True)
    photographer = models.ForeignKey(
        Photographer, on_delete=models.CASCADE, null=True, related_name="photos")
    date = models.DateField()
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"{self.title} - {self.photographer}, {self.date}"
