from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Project, ProjectProcess
from .models import Environ, EnvironProcess
from django.shortcuts import redirect
from django.contrib import messages
from .tasks import generate_env, create_env, build_front, merge_release
from git import Repo
import os
from django.conf import settings
from main.models import Task2User, Commit, Task


@login_required
def list(request):
    envs = Environ.objects.filter(user=request.user)
    cnt = Environ.objects.filter(user=request.user).count()
    if cnt == 1:
        return redirect('/env/detail/%s' % envs[0].id)
    return render(request, 'env/list.html', {'envs': envs})


@login_required
def detail(request, id):
    env = Environ.objects.get(pk=id)
    envs = Environ.objects.filter(user=request.user).exclude(id=id)
    tasks = []
    mytasks = []
    tmptasks = Task.objects.filter(project=env.project)
    tmpmytasks = Task2User.objects.filter(project=env.project, user=request.user)
    for it in tmpmytasks:
        mytasks.append(it.task)
    for t in tmptasks:
        if t not in mytasks:
            tasks.append(t)
    print(tasks)
    print(tmptasks)
    commits = Commit.objects.filter(user=request.user, project=env.project)
    return render(request, 'env/detail.html', {'env': env, 'envs': envs, 'tasks': tasks, 'commits': commits, 'mytasks': mytasks, 'ssh_login':settings.SSH_LOGIN, 'ssh_password': settings.SSH_PASSWORD, 'domain': settings.DOMAIN, "ssh_port": settings.SSH_PORT})



@login_required
def do_build_front(request, id):
    env = Environ.objects.get(pk=id)
    cnt = 0
    for ep in EnvironProcess.objects.filter(env=env,name='frontend'):
        cnt = cnt + 1
        build_front.delay(ep.id)
    if cnt > 0:
        messages.success(
            request, 'Сборка запущена. Это может занять 1-2 мин!')
    else:
        messages.success(
            request, 'Этот проект не включает фронтенд!')        
    return redirect('/env/detail/%s' % id)


@login_required
def pre_create(request, id):
    project = Project.objects.get(pk=id)
    return render(request, 'env/pre_create.html', {'project':project})


@login_required
def create(request, id):
    if not create_env(id,request.user.id):
        messages.success(
            request, 'Ошибка. Эта область уже создана!')
    else:
        messages.success(
            request, 'Рабочая область создается. Это может занять 1-2 мин!')
    return redirect('/env/list')


@login_required
def pre_remove(request, id):
    env = Environ.objects.get(pk=id)
    path = os.path.join(settings.WORK_DIR, env.name)
    diff = []
    try:
        repo = Repo(path)
        hcommit = repo.head.commit
        diff = hcommit.diff(None) 
    except:
        pass 
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

def do_merge(request, id):
    env = Environ.objects.get(pk=id)
    env.state = 'clean'
    env.save()
    merge_release.delay(id)
    messages.success(
        request, 'Данные смержены!')
    return redirect('/control')