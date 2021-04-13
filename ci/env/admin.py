from django.contrib import admin
from .models import *


class EnvironProcessInline(admin.TabularInline):
    model = EnvironProcess
    list_display = ['name']

@admin.register(Environ)
class EnvironAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'state']
    inlines = [EnvironProcessInline, ]

@admin.register(EnvironProcess)
class EnvironProcessAdmin(admin.ModelAdmin):
    list_display = ['name', 'port', 'env', 'path', 'command']