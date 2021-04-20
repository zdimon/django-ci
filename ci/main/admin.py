from django.contrib import admin

from .models import *

class FileInline(admin.TabularInline):
    model = File
    list_display = ['title', 'image', 'thumb']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']


@admin.register(Env)
class EnvAdmin(admin.ModelAdmin):
    list_display = ['email', 'link']




@admin.register(Maket)
class MaketAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'project']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'is_done', 'project', 'budget']
    inlines = [FileInline, ]
    list_editable = ['budget']
    list_filter = ['project']


@admin.register(Task2User)
class Task2UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'project']


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'task', 'created_at']

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'created_at']
