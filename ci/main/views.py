import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import EnvForm
from django.shortcuts import redirect
from django.conf import settings
from .models import Env
from .tasks import normalize_email, git_push, git_merge_with_master
from .models import Env, Task, Task2User, Commit, Maket, Page
from project.models import Project
from git import Repo
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from env.models import Environ
from django.utils import translation

def set_language(request):
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        translation.activate(lang_code)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def env(request):
    error = None
    message = None
    env = None
    try:
        env = Env.objects.get(user=request.user)
    except:
        error = 'Ваша Рабочая область пока не создана.'

    tasks = Task2User.objects.filter(user=request.user)
    commits = Commit.objects.filter(user=request.user)

    if request.method == 'POST':
        form = EnvForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.user = request.user
            obj.save()
            # import pdb
            # pdb.set_trace()
            message = 'Рабочая область создана!'
            return redirect('/env')
    else:
        form = EnvForm(initial={'email': request.user.username})

    return render(request, 'env.html', {"error": error, "env": env, "form": form, "message": message, "tasks": tasks, "commits": commits})


def index(request):
    page = Page.objects.get(alias='main')
    if request.user.is_authenticated:
        return redirect('/project/list')
    projects = Project.objects.all()
    return render(request, 'index.html', {"projects": projects, 'page':page})


def instr(request):
    return render(request, 'instr.html')


@csrf_exempt
def hook(request):
    data = json.loads(request.body)
    if data["action"] == 'closed':
        print(data["pull_request"])
    return HttpResponse('Ok')


def tasks(request):
    tasks = Task.objects.filter(is_done=False).order_by('-id')
    return render(request, 'tasks.html', {"tasks": tasks})


def done(request, id):
    env = Env.objects.get(pk=id)
    link = '%s.%s' % (normalize_email(env.email), settings.DOMAIN)
    return render(request, 'done.html', {'link': link})


def info(request):
    return render(request, 'info.html')


def take_task(request, id):
    task = Task.objects.get(pk=id)
    env = Environ.objects.get(project=task.project,user=request.user)
    try:
        Task2User.objects.get(user=request.user, task=task)
        messages.success(
            request, 'Эта задача уже в работе!')
        return redirect('/env/detail/%s#mytask' % env.id)
    except:
        t2u = Task2User()
        t2u.user = request.user
        t2u.task = task
        t2u.project = env.project
        t2u.save()
        messages.success(
            request, 'Задача взята в работу и помещена в раздел "Взятые задачи"')
        return redirect('/env/detail/%s#mytask' % env.id)


def del_task(request, id):
    task = Task.objects.get(pk=id)
    t2u = Task2User.objects.get(task=task,user=request.user)
    env = Environ.objects.get(project=task.project,user=request.user)
    if t2u.user == request.user:
        t2u.delete()
        messages.success(
            request, 'Задача удалена')
    return redirect('/env/detail/%s#mytask' % env.id)


def done_task(request, id):
    t = Task.objects.get(pk=id)
    task = Task2User.objects.get(task=t,user=request.user)
    return render(request, 'done_task.html', {"task": task})


def end_task(request, id):

    #origin = repo.remote(name='origin')
    # origin.push()
    task = Task2User.objects.get(pk=id)
    env = Environ.objects.get(user=request.user,project=task.project)
    if task.user == request.user:
        git_push.delay(env.id, id)
        task.is_done = True
        task.save()
        c = Commit()
        c.user = request.user
        c.task = task.task
        c.title = task.task.title
        c.save()
        messages.success(
            request, 'Спасибо! Ваши изменения зафиксированы и отправлены на проверку.')
    return redirect('/env/detail/%s' % env.id)

def merge_master(request, id):
    git_merge_with_master.delay(id)
    messages.success(
        request, 'Отлично! Теперь Ваш репозиторий синхронизирован с актуальной версией проекта (веткой master).')
    return redirect('/control')

def maket(request,id):
    project = Project.objects.get(pk=id)
    items = Maket.objects.filter(project=project)
    return render(request, 'maket.html', {"items": items})
