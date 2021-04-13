from django.contrib.auth.models import User
import subprocess
from main.utils import run_command
from django.conf import settings
import os
from main.utils import run_command
from celery.decorators import task
from .utils import release_django_conf, release_nginx_conf, frontend_conf
from main.tasks import restart

@task()
def clear_origin(poj_id):
    from project.models import Project
    prj = Project.objects.get(pk=poj_id)
    env_path = os.path.join(settings.ORIGIN_DIR, prj.name)
    bashCommand = "sudo rm -r %s" % env_path
    run_command(bashCommand)

@task()
def make_release_server(poj_id):
    release_django_conf(poj_id)
    release_nginx_conf(poj_id)
    frontend_conf(poj_id)
    restart()

@task()
def clone_origin(poj_id):
    import time
    time.sleep(1)
    from project.models import Project
    prj = Project.objects.get(pk=poj_id)
    print('Cloning origin from %s' % prj.git)
    path = os.path.join(settings.ORIGIN_DIR, prj.name)
    os.mkdir(path)
    os.chdir(path)
    command = f'git clone {prj.git} .'
    run_command(command)
    print('Cheking',os.path.join(path,'install'))
    if os.path.isfile(os.path.join(path,'install')):
        os.chdir(path)
        run_command('bash install')