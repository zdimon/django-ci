from django.db.models.deletion import CASCADE
from project.models import Project
from django.db.models.signals import pre_delete
from .tasks import normalize_email
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Max
from .tasks import create_dir, git_clone, nginx_conf, supervisor_conf, clear_env, normalize_email
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from image_cropping.fields import ImageRatioField, ImageCropField
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from tinymce.models import HTMLField


class Page(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=250)
    alias = models.CharField(verbose_name=_('Alias'), max_length=50)
    content = HTMLField(null=True, blank=True, verbose_name=_('Content'))

class Env(models.Model):
    project = models.ForeignKey('project.Project',on_delete=CASCADE)
    email = models.CharField(verbose_name='Логин', max_length=60, unique=True)
    port = models.IntegerField(default=8080)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def link_url(self):
        return "http://%s.%s" % (normalize_email(self.email), settings.DOMAIN)

    @ property
    def link(self):
        return mark_safe('<a target=_blank href="http://%s.%s">Ссылка на рабочую область</a>' % (normalize_email(self.email), settings.DOMAIN))

    @ classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            maxp = Env.objects.aggregate(Max('port'))
            print(maxp)
            instance.port = maxp["port__max"]+1
            instance.save()
            create_dir(instance.id)
            git_clone.delay(instance.id)
            nginx_conf(instance.id)
            supervisor_conf(instance.id)
            # restart()

class EnvProcess(models.Model):
    name = models.CharField(verbose_name='Название', max_length=250, unique=True)
    status =  models.CharField(verbose_name='Статус', max_length=50, default='создается')
    env = models.ForeignKey(Env, on_delete=models.CASCADE)


def pre_delete_handler(sender, instance, using, **kwargs):
    clear_env.delay(normalize_email(instance.email))


post_save.connect(Env.post_create, sender=Env)
pre_delete.connect(pre_delete_handler, sender=Env)


class Task(models.Model):

    TYPE = (
        ("бекенд", "бекенд"),
        ("фронтенд", "фронтенд"),
    )

    HARD = (
        ("простая", "простая"),
        ("средняя", "средняя"),
        ("сложная", "сложная"),
    )

    title = models.CharField(max_length=250)
    type = models.CharField(max_length=50, choices=TYPE, default='фронтенд')
    hard = models.CharField(max_length=50, choices=TYPE, default='простая')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    desc = HTMLField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    budget = models.IntegerField(default=0)

    @property
    def get_status(self):
        if self.is_done:
            return 'не выполнено'
        else:
            return 'выполнено'

    def __str__(self):
        return self.title


class Maket(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=250)
    image = ImageCropField(upload_to='files')
    cropping = ImageRatioField('image', '150x150')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, default=1)

    @property
    def small_image_url(self):
        try:
            return get_thumbnailer(self.image).get_thumbnail({
                'size': (150, 150),
                'box': self.cropping,
                'crop': 'smart',
            }).url
        except Exception as e:
            print(e)
            return SERVER_NAME + 'static/noimage.png'


class File(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=250, blank=True, null=True)
    image = ImageCropField(upload_to='files')
    task = models.ForeignKey(
        Task, verbose_name="Задача", on_delete=models.CASCADE)
    cropping = ImageRatioField('image', '80x80')

    @property
    def small_image_url(self):
        try:
            return get_thumbnailer(self.image).get_thumbnail({
                'size': (80, 80),
                'box': self.cropping,
                'crop': 'smart',
            }).url
        except Exception as e:
            return SERVER_NAME + 'static/noimage.png'


class Task2User(models.Model):
    user = models.ForeignKey("account.Customer", verbose_name=_(
        "Пользователь"), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name=_(
        "Задача"), on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    @property
    def get_status(self):
        if self.is_done:
            return 'Выполнено'
        else:
            return 'В работе'


class Commit(models.Model):
    user = models.ForeignKey("account.Customer", verbose_name=_(
        "Пользователь"), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name=_(
        "Задача"), on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=_(
        "Задача"), on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(verbose_name='Заголовок', max_length=250)

class Log(models.Model):
    user = models.ForeignKey("account.Customer", verbose_name=_(
        "Пользователь"), on_delete=models.CASCADE)
    action = models.CharField(verbose_name='Действие', max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)