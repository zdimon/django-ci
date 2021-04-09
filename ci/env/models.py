from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db.models import Max
from django.db.models.signals import post_save
from .utils import clear_work_dir, restart
from django.db.models.signals import pre_delete
from .tasks import generate_env
from project.models import ProjectProcess


class Environ(models.Model):
    project = models.ForeignKey('project.Project',on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название рабочей области', help_text=_('должно быть уникальным, поэтому мы добавили ваш логин и id проекта'), max_length=60, unique=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name

    @property
    def link_url(self):
        return "http://%s.%s" % (self.name, settings.DOMAIN)

    @ property
    def link(self):
        return mark_safe('<a target=_blank href="http://%s.%s">Ссылка на рабочую область</a>' % (self.name, settings.DOMAIN))

    @ classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            for p in ProjectProcess.objects.filter(project=instance.project):
                ep = EnvironProcess()
                ep.env = instance
                ep.envproc = p
                ep.path = p.path
                ep.name = p.name
                ep.command = p.command
                ep.save()
            generate_env(instance.id)
            #generate_env(instance.id)
            #git_clone(instance.id)
            #nginx_conf(instance.id)
            #supervisor_conf(instance.id)
            # restart()

class EnvironProcess(models.Model):
    name = models.CharField(verbose_name='Название', max_length=250, unique=True)
    status =  models.CharField(verbose_name='Статус', max_length=50, default='создается')
    env = models.ForeignKey(Environ, on_delete=models.CASCADE)
    path =  models.CharField(verbose_name='Каталог', max_length=250)
    command =  models.CharField(verbose_name='Каталог', max_length=250, default='')
    port = models.IntegerField(default=8080)
    envproc = models.ForeignKey('project.ProjectProcess', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            maxp = EnvironProcess.objects.aggregate(Max('port'))
            # print(maxp)
            instance.port = maxp["port__max"]+1
            instance.save()

def pre_delete_handler(sender, instance, using, **kwargs):
    clear_work_dir(instance)
    restart()


# post_save.connect(EnvironProcess.post_create, sender=EnvironProcess)
post_save.connect(Environ.post_create, sender=Environ)
pre_delete.connect(pre_delete_handler, sender=Environ)