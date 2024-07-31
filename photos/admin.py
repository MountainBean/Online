from django.contrib import admin

from .models import Photographer, Photo


class PhotoAdmin(admin.ModelAdmin):
    list_filter = ("title", "location", "date", "photographer")
    list_display = ("title", "location", "date", "photographer")
    prepopulated_fields = {
        "slug": ("title",)
    }


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Photographer)
