from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Project, ProjectProcess
from .models import Environ, EnvironProcess
from django.shortcuts import redirect
from django.contrib import messages
from .tasks import generate_env, create_env
from git import Repo
import os
from django.conf import settings


@login_required
def list(request):
    envs = Environ.objects.filter(user=request.user)
    return render(request, 'env/list.html', {'envs':envs})

@login_required
def detail(request,id):
    env = Environ.objects.get(pk=id)
    return render(request, 'env/detail.html', {'env':env})


@login_required
def pre_create(request,id):
    project = Project.objects.get(pk=id)
    return render(request, 'env/pre_create.html', {'project':project})


@login_required
def create(request,id):
    if not create_env(id,request.user.id):
        messages.success(
            request, 'Ошибка. Эта область уже создана!')
    else:
        messages.success(
            request, 'Рабочая область создается. Это может занять 1-2 мин!')
    return redirect('/env/list')


@login_required
def pre_remove(request,id):
    env = Environ.objects.get(pk=id)
    path = os.path.join(settings.WORK_DIR, env.name)
    repo = Repo(path)
    hcommit = repo.head.commit
    diff = hcommit.diff(None)  
    # import pdb; pdb.set_trace()
    print(diff)
    return render(request, 'env/pre_remove.html', {'env':env, 'diff': diff})

def remove(request,id):
    env = Environ.objects.get(pk=id)
    #  if env.user == request.user:
    env.delete()
    messages.success(
        request, 'Рабочая область удалена!')
    return redirect('/env/list')