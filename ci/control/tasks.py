from django.conf import settings
import os
import git
from celery.decorators import task
import subprocess
from main.utils import run_command, normalize_email
from env.models import Environ
from git import Repo
from env.utils import save_commit


def git_pull(env_id):
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    os.chdir(path)
    out = run_command('git pull origin master')
    #out = run_command('git push')
    return out


def git_commit(env_id):  
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    os.chdir(path)
    run_command('git add .')
    comment = 'commit from %s project %s' % (env.user.username, env.project.name)
    run_command('git commit -m "%s"' % comment)
    d = run_command('git push')
    print(d)
    # repo = Repo(path)
    # t = repo.head.commit.tree
    #if repo.git.diff(t):
    # print('Make commit')
    # repo.git.add(update=True)
    # comment = 'commit from %s project %s' % (env.user.username, env.project.name)
    # r = repo.index.commit(comment)
    # env.state = 'edited'
    # env.save()
    # save_commit(comment, env)
    # os.chdir(path)
    # out = run_command('git push')
    return {"error": None, "output": f'Данные закомичены. {d["output"]} '}
    # else:
    #     return {"error": None, "output": 'Нечего комитить.'}

    #print(r)
    # os.chdir(path)
    # command = "git add ."
    # out = run_command(command)
    # bname = 'devel-%s' % env.name
    # command = 'bash git commit -m "commit to %s"' % bname
    # print(command)
    # out = run_command(command)
    # return out

    



def git_push(env_id):
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    os.chdir(path)
    bname = 'devel-%s' % env.name
    command = 'git push --set-upstream origin %s' % bname
    # command = 'git push'
    out = run_command(command)
    return out


def git_status(env_id):
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    os.chdir(path)
    out = run_command('git status')
    return out


def git_diff(env_id):
    env = Environ.objects.get(pk=env_id)
    path = os.path.join(settings.WORK_DIR, env.name)
    os.chdir(path)
    out = run_command('git diff')
    return out
