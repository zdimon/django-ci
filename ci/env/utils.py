from django.contrib.auth.models import User
import subprocess
from main.utils import run_command
from django.conf import settings
import os
import git

def nginx_conf(env_id):
    from .models import Environ, EnvironProcess
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.BASE_DIR, 'tpl', 'nginx_vhost.conf')
    with open(path, 'r') as f:
        tpl = f.read()

    tpl = tpl.replace('%media_path%', env.project.media_path)
    sname = '%s.%s' % (env.name, settings.DOMAIN)
    tpl = tpl.replace('%server_name%', sname)
    dj = EnvironProcess.objects.get(env=env,name='django')
    tpl = tpl.replace('%port%', str(dj.port))
    conf_path = os.path.join(
        settings.BASE_DIR,'env-conf','nginx', env.name)
    with open(conf_path, 'w+') as f:
        f.write(tpl) 

       
def frontend_conf(env_id):
    from .models import Environ, EnvironProcess
    env = Environ.objects.get(pk=env_id)
    try:
        envp = EnvironProcess.objects.get(env=env,name='frontend')
        path = os.path.join(settings.BASE_DIR, 'tpl', 'frontend.conf')
        with open(path, 'r') as f:
            tpl = f.read()
        sname = '%s.frontend.%s' % (env.name, settings.DOMAIN)
        tpl = tpl.replace('%name%', sname)
        # tpl = tpl.replace('%port%', str(envp.port))
        tpl = tpl.replace('%user%', settings.USER)
        prj_dir = os.path.join(settings.WORK_DIR, env.name, envp.path)
        tpl = tpl.replace('%prj_dir%', prj_dir)
        tpl = tpl.replace('%ci_dir%', str(settings.BASE_DIR))
        tpl = tpl.replace('%command%', envp.command)
        filename = '%s-frontend.conf' % env.name
        conf_path = os.path.join(
             settings.BASE_DIR, 'env-conf', 'supervisor', filename)
        with open(conf_path, 'w+') as f:
            f.write(tpl)
    except Exception as e:
        print(e)

        
def django_conf(env_id):
    from .models import Environ, EnvironProcess
    env = Environ.objects.get(pk=env_id)
    envp = EnvironProcess.objects.get(env=env, name='django')
    path = os.path.join(settings.BASE_DIR, 'tpl', 'django.conf')
    with open(path, 'r') as f:
        tpl = f.read()
    sname = '%s.django.%s' % (env.name, settings.DOMAIN)
    tpl = tpl.replace('%name%', sname)
    tpl = tpl.replace('%port%', str(envp.port))
    if env.project.venv_path:
        prj_dir = os.path.join(settings.WORK_DIR, env.name, env.project.venv_path)
    else:
        prj_dir = os.path.join(settings.WORK_DIR, env.name)
    
    tpl = tpl.replace('%prj_dir%', prj_dir)
    tpl = tpl.replace('%ci_dir%', str(settings.BASE_DIR))
    tpl = tpl.replace('%user%', settings.USER)
    if env.project.venv_path:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.WORK_DIR, env.name, env.project.venv_path, 'venv'))
    else:
        tpl = tpl.replace('%env_dir%', os.path.join(settings.WORK_DIR, env.name, 'venv'))        
    filename = '%s-django.conf' % env.name
    conf_path = os.path.join(
        settings.BASE_DIR, 'env-conf', 'supervisor', filename)
    with open(conf_path, 'w+') as f:
        f.write(tpl)


def clone_origin(poj_id):
    from project.models import Project
    prj = Project.objects.get(pk=poj_id)
    print('Cloning origin from %s' % prj.git)
    path = os.path.join(settings.ORIGIN_DIR, prj.name)
    try:
        os.mkdir(path)
    except:
        pass
    os.chdir(path)
    run_command("git clone %s %s" % (prj.git,prj.name))
    
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
    from .models import Environ
    env = Environ.objects.get(pk=env_id)
    prj = env.project
    path_to = os.path.join(settings.WORK_DIR, env.name)
    path_from = os.path.join(settings.ORIGIN_DIR, prj.name)
    bashCommand = "cp -r %s/. %s" % (path_from, path_to)
    print('Pulling origin')
    g = git.cmd.Git(path_from)
    g.pull()
    print('Coping project')
    run_command(bashCommand)
    git_create_branch(env_id)
    #copy_frontend(env_id)
    #django_conf(env_id)
    # register_user(env_id)
    #restart()





def create_dir(env_id):
    from env.models import Environ
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    print('Creating work dir %s' % path)
    try:
        os.mkdir(path)
    except:
        pass


   