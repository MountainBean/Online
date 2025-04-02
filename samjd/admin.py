from django.contrib import admin
from .models import ProjectImage, Project, Cert

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(ProjectImage)
admin.site.register(Project)
admin.site.register(Cert)

