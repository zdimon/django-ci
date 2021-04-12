from django.shortcuts import render
from .models import Project
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from env.models import Environ
from django.shortcuts import redirect


@login_required
def pre_remove(request,id):
    projects = Project.objects.get(pk=id)
    env = Environ.objects.filter(user=request.user, project=project)
    return redirect(f'/env/pre_remove/{env.id}')




@login_required
def list(request):
    projects = Project.objects.all()
    eid = []
    for e in Environ.objects.filter(user=request.user):
        eid.append(e.project.id)
    return render(request, 'project/list.html', {"projects": projects, "eid": eid})
