# Generated by Django 3.2 on 2021-04-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20210412_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectprocess',
            name='path',
        ),
        migrations.AddField(
            model_name='project',
            name='venv_path',
            field=models.CharField(default='', max_length=250, verbose_name='Путь к ВО'),
        ),
    ]
