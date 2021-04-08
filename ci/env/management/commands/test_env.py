from django.core.management.base import BaseCommand, CommandError
from env.models import Environ
from project.models import Project
from django.contrib.auth.models import User

class Command(BaseCommand):
   
    def handle(self, *args, **options):
        print('Del env')
        Environ.objects.all().delete()
        user = User.objects.all().order_by('-id').first()
        prj = Project.objects.all().first()
        e = Environ()
        e.user = user
        e.project = prj
        e.save()