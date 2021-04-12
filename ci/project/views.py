from django.shortcuts import render
from .models import Project
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from env.models import Environ


@login_required
def list(request):
    projects = Project.objects.all()
    eid = []
    for e in Environ.objects.filter(user=request.user):
        eid.append(e.project.id)
    return render(request, 'project/list.html', {"projects": projects, "eid": eid})
