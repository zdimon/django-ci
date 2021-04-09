from django.core.management.base import BaseCommand, CommandError
from env.models import Environ
from project.models import Project
from django.contrib.auth.models import User
import os
from django.conf import settings
import getpass
from env.tasks import restart


def edit_supervisor_conf():
    search = 'include /etc/nginx/conf.d/*.conf;'
    repl = 'include /etc/nginx/conf.d/*.conf; \n include %s/*.conf;' % os.path.join(settings.BASE_DIR,'ci-conf')
    path = '/etc/nginx/nginx.conf'
    print('Edit %s' % path) 
    with open(path, 'r') as f:
        tpl = f.read();
    tpl = tpl.replace(search,repl)
    with open(path,'w') as f:
        f.write(tpl)


def edit_nginx_conf():
    search = 'include /etc/nginx/conf.d/*.conf;'
    repl = 'include /etc/nginx/conf.d/*.conf; \n include %s/*.conf;' % os.path.join(settings.BASE_DIR,'env-conf', 'nginx')
    path = '/etc/nginx/nginx.conf'
    print('Edit %s' % path) 
    with open(path, 'r') as f:
        tpl = f.read();
    tpl = tpl.replace(search,repl)
    with open(path,'w') as f:
        f.write(tpl)

def make_conf():
    with open(os.path.join(settings.BASE_DIR,'ci-conf','django-ci.conf',), 'r') as f:
        tpl = f.read()
        tpl = tpl.replace('%base_dir%', str(settings.BASE_DIR))
        tpl = tpl.replace('%user%', getpass.getuser())
        
    with open(os.path.join(settings.BASE_DIR,'ci-conf','django-ci.conf',), 'w') as f:
        f.write(tpl)


def create_dirs():
    if not os.path.isdir(os.path.join(settings.BASE_DIR,'logs')):
        print('Creating log dir')
        os.mkdir(os.path.join(settings.BASE_DIR,'logs'))
    if not os.path.isdir(os.path.join(settings.BASE_DIR,'env-conf')):
        print('Creating conf dir')
        os.mkdir(os.path.join(settings.BASE_DIR,'env-conf'))
        os.mkdir(os.path.join(settings.BASE_DIR,'env-conf','nginx'))
        os.mkdir(os.path.join(settings.BASE_DIR,'env-conf','supervisor'))
class Command(BaseCommand):
   
    def handle(self, *args, **options):
        print('Installation...')
        create_dirs()
        make_conf()
        edit_nginx_conf()
        restart()
     