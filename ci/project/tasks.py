from django.contrib.auth.models import User
import subprocess
from main.utils import run_command
from django.conf import settings
import os
from main.utils import run_command
from celery.decorators import task

@task()
def clear_origin(poj_id):
    from project.models import Project
    prj = Project.objects.get(pk=poj_id)
    env_path = os.path.join(settings.ORIGIN_DIR, prj.name)
    bashCommand = "sudo rm -r %s" % env_path
    run_command(bashCommand)


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