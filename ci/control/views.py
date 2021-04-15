from main.utils import run_command
from django.shortcuts import render
from env.models import Environ, EnvironProcess
from project.models import Project
from .tasks import git_pull, git_status, git_push, git_diff, git_commit
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import os
from main.utils import run_command
import sh

def control(request):
    envs = Environ.objects.all()
    projects = Project.objects.all()

    return render(request, 'control/list.html', {"envs": envs, "projects": projects})


def do_pull(request, id):
    rez = git_pull(id)
    return JsonResponse(rez)


def do_push(request, id):
    rez = git_push(id)
    return JsonResponse(rez)


def do_status(request, id):
    rez = git_status(id)
    return JsonResponse(rez)


def do_diff(request, id):
    rez = git_diff(id)
    return JsonResponse(rez)


def do_commit(request, id):
    rez = git_commit(id)
    return JsonResponse(rez)


def error_log(request, id):
    env = Environ.objects.get(pk=id)
    lname = f'{env.name}.django.{settings.DOMAIN}-err.log'
    path = os.path.join(settings.BASE_DIR,'logs',lname)
    with open(path, 'r') as f:
        t = f.read()
    rez = {"output": t}
    return JsonResponse(rez)

def clear_log(request, id):
    env = Environ.objects.get(pk=id)
    lname = f'{env.name}.django.{settings.DOMAIN}'
    logname = f'{env.name}.django.{settings.DOMAIN}-err.log'
    path = os.path.join(settings.BASE_DIR, 'logs', lname)
    logpath = os.path.join(settings.BASE_DIR,'logs', logname)
    command = "sudo supervisorctl -c /etc/supervisor/supervisord.conf stop %s" % lname
    run_command(command)
    
    command = "rm -f %s" % logpath
    print(command)
    run_command(command)
    command = "sudo supervisorctl -c /etc/supervisor/supervisord.conf start %s" % lname
    run_command(command)
    rez = {"output": 'Ok'}
    return JsonResponse(rez)