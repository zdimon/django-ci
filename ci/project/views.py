from django.shortcuts import render
from .models import Project
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def list(request):
    projects = Project.objects.all()
    return render(request, 'project/list.html', {"projects": projects})
