from django.db import models
from django.utils.html import mark_safe
from easy_thumbnails.files import get_thumbnailer
from image_cropping.fields import ImageRatioField, ImageCropField
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete

class Project(models.Model):
    title = models.CharField(verbose_name='Название', max_length=160, unique=True)
    name = models.CharField(verbose_name='Название (лат)', max_length=160, unique=True)
    desc = models.TextField(verbose_name='Описание')
    image = ImageCropField(upload_to='files')
    cropping = ImageRatioField('image', '150x150')
    git = models.CharField(verbose_name='git репозиторий', max_length=250, unique=True)
    git_url = models.CharField(verbose_name='url git репозитория', max_length=250, default='')
    media_path =  models.CharField(verbose_name='Путь к медиа', max_length=250, default='')
    venv_path =  models.CharField(verbose_name='Путь к ВО', max_length=250, default='', null=True, blank=True)
    
    def __str__(self):
        return self.title

    @property
    def small_image_url(self):
        try:
            return get_thumbnailer(self.image).get_thumbnail({
                'size': (80, 80),
                'box': self.cropping,
                'crop': 'smart',
            }).url
        except Exception as e:
            return '/static/noimage.png'

    @property
    def small_image_tag(self):
        return mark_safe(f'<img src="{self.small_image_url}">')

class ProjectProcess(models.Model):
    PROC_CHOICES = (
        ("django", "django"),
        ("celery", "celery"),
        ("frontend", "frontend"),
        ("socket", "socket"),
    )
    name = models.CharField(choices=PROC_CHOICES,verbose_name='Название', max_length=60, default='django')
    command =  models.CharField(verbose_name='Команда', max_length=250)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    path =  models.CharField(verbose_name='Каталог', max_length=250, null=True, blank=True)    

    def __str__(self):
        return self.name
    

from .tasks import clone_origin, clear_origin


def post_create_handler(sender, instance, created, *args, **kwargs):
    if created:
        clone_origin.delay(instance.pk)


def pre_delete_handler(sender, instance, using, **kwargs):
    clear_origin(instance.pk)    


post_save.connect(post_create_handler, sender=Project)
pre_delete.connect(pre_delete_handler, sender=Project)