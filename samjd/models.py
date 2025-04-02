from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

class ProjectImage(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to="project_images")
    alt_text = models.TextField()

    def __str__(self):
        return self.title

class Project(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subheading = models.CharField(max_length=512, blank=True, null=True)
    header_image = ForeignKey(ProjectImage, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField()
    blurb = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(default="", null=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Cert(models.Model):
    url = models.URLField(null=True)
    title = models.CharField(max_length=256)
    image = models.URLField(null=True)

    def __str__(self):
        return self.title
