from django.contrib import admin
from .models import *

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['small_image_tag','title', 'git']


@admin.register(ProjectProcess)
class ProjectProcessAdmin(admin.ModelAdmin):
    list_display = ['name', 'command', 'project', 'path']