from django.shortcuts import render
from .models import Project
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from env.models import Environ
from django.shortcuts import redirect
from .tasks import make_release_server
from django.conf import settings


@login_required
def pre_remove(request,id):
    project = Project.objects.get(pk=id)
    env = Environ.objects.get(user=request.user, project=project)
    return redirect(f'/env/pre_remove/{env.id}')


@login_required
def make_release(request,id):
    project = Project.objects.get(pk=id)
    messages.success(
        request, 'Релизный сервер создается.')
    make_release_server.delay(id)
    url = 'http://release-%s.%s' % (project.name, settings.DOMAIN)
    project.release_url = url
    project.save()
    return redirect(f'/control')

@login_required
def list(request):
    projects = Project.objects.all()
    eid = []
    for e in Environ.objects.filter(user=request.user):
        eid.append(e.project.id)
    return render(request, 'project/list.html', {"projects": projects, "eid": eid})
