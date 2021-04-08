from django.contrib.auth.models import User
import subprocess
from main.utils import run_command
from django.conf import settings
import os
import git

def clone_origin(poj_id):
    from project.models import Project
    prj = Project.objects.get(pk=poj_id)
    print('Cloning origin from %s' % prj.git)
    
def git_create_branch(env_id):
    from .models import Environ
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    os.chdir(path)
    bname = 'devel-%s' % env.name
    run_command("git branch %s" % bname)
    run_command("git checkout %s" % bname)
    run_command("git push --set-upstream origin %s" % bname)


def git_clone(env_id):
    print('Cloning project')
    from .models import Environ
    env = Environ.objects.get(pk=env_id)
    prj = env.project
    path_to = os.path.join(settings.WORK_DIR, env.name)
    path_from = os.path.join(settings.ORIGIN_DIR, prj.name)
    bashCommand = "cp -r %s/. %s" % (path_from, path_to)
    g = git.cmd.Git(path_from)
    g.pull()
    run_command(bashCommand)
    git_create_branch(env_id)
    #copy_frontend(env_id)
    #django_conf(env_id)
    # register_user(env_id)
    #restart()


def clear_work_dir(env):
    print('Removing work dir')
    env_path = os.path.join(settings.WORK_DIR, env.name)
    bashCommand = "sudo rm -r %s" % env_path
    run_command(bashCommand)


def create_dir(env_id):
    from env.models import Environ
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    print('Creating work dir %s' % path)
    os.mkdir(path)