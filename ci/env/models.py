from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db.models import Max
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from .tasks import generate_env, clear_work_dir, restart
from project.models import ProjectProcess


class Environ(models.Model):
    STATE = (
        ("clean", _("without changes")),
        ("edited", _("with changes")),
    )
    project = models.ForeignKey('project.Project',on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), help_text=_('must be unique'), max_length=60, unique=True)
    status = models.CharField(verbose_name=_('Status'), max_length=60, default='creating')
    state = models.CharField(verbose_name='Состояние', max_length=60, default='clean', choices=STATE)
    user = models.ForeignKey(
        "account.Customer", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name

    @property
    def link_url(self):
        return "http://%s.%s" % (self.name, settings.DOMAIN)

    @property
    def get_work_dir(self):
        return "work/%s" % (self.name,)

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
                ep.name = p.name
                ep.path = p.path
                ep.command = p.command
                ep.save()
            generate_env.delay(instance.id)
            #generate_env(instance.id)
            #git_clone(instance.id)
            #nginx_conf(instance.id)
            #supervisor_conf(instance.id)
            # restart()

class EnvironProcess(models.Model):
    name = models.CharField(verbose_name='Название', max_length=250)
    status =  models.CharField(verbose_name='Статус', max_length=50, default='создается')
    env = models.ForeignKey(Environ, on_delete=models.CASCADE)
    path =  models.CharField(verbose_name='Каталог', max_length=250, null=True, blank=True)
    command =  models.CharField(verbose_name='Комманда', max_length=250, default='')
    port = models.IntegerField(default=8080)
    envproc = models.ForeignKey('project.ProjectProcess', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            maxp = EnvironProcess.objects.aggregate(Max('port'))
            print(maxp)
            instance.port = maxp["port__max"]+1
            instance.save()

def pre_delete_handler(sender, instance, using, **kwargs):
    clear_work_dir.delay(instance.name)
    


post_save.connect(EnvironProcess.post_create, sender=EnvironProcess)
post_save.connect(Environ.post_create, sender=Environ)
pre_delete.connect(pre_delete_handler, sender=Environ)