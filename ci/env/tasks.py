from django.conf import settings
import os
import git
from celery.decorators import task
from django.contrib.auth.models import User
import subprocess
from main.utils import run_command
from .utils import create_dir, clear_work_dir, git_create_branch, git_clone, nginx_conf, restart, django_conf, frontend_conf



@task()
def generate_env(env_id):
    from .models import Environ
    env = Environ.objects.get(pk=env_id)
    print('Creating work env %s!' % env.id)
    create_dir(env_id)
    git_clone(env_id)
    git_create_branch(env_id)
    django_conf(env_id)
    frontend_conf(env_id)
    nginx_conf(env_id)
    restart()


def create_env(project_id, user_id):
    from project.models import Project, ProjectProcess
    from .models import Environ, EnvironProcess
    project = Project.objects.get(pk=project_id)
    user = User.objects.get(pk=user_id)
    ename = f'{user.username}-{project.id}' 
    try:
        env = Environ.objects.get(name=ename)
        return False
    except:
        env = Environ()
        env.project = project
        env.name = ename
        env.user = user
        env.save()
        #generate_env(env.id)
        return True
    
