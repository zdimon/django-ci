from django.core.management.base import BaseCommand, CommandError
from env.models import Environ
from project.models import Project, ProjectProcess
from django.contrib.auth.models import User
from account.models import Customer
import os
from django.conf import settings
import getpass
from env.tasks import restart

class Command(BaseCommand):
   
    def handle(self, *args, **options):
        print('Load user ...')
        Customer.objects.all().delete()
        c = Customer()
        c.username = 'zdimon'
        c.is_superuser = True
        c.is_staff = True
        c.set_password('1')
        c.save()
        print('Load test ...')
        Project.objects.all().delete()
        p = Project()
        p.name = 'start-django'
        p.title = 'Test django project'
        p.git = 'git@github.com:zdimon/start-django.git'
        p.media_path = '/home/zdimon/www/django-ci/work/media'
        p.venv_path = ''
        p.save()

        pp = ProjectProcess()
        pp.project = p
        pp.name = 'django'
        pp.command = './manage.py runserver'
        pp.save()
       