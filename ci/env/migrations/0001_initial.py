# Generated by Django 3.2 on 2021-04-12 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '__first__'),
        ('account', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Environ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='должно быть уникальным, поэтому мы добавили ваш логин и id проекта', max_length=60, unique=True, verbose_name='Название рабочей области')),
                ('status', models.CharField(default='создается', max_length=60, verbose_name='Статус')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
        ),
        migrations.CreateModel(
            name='EnvironProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('status', models.CharField(default='создается', max_length=50, verbose_name='Статус')),
                ('command', models.CharField(default='', max_length=250, verbose_name='Каталог')),
                ('port', models.IntegerField(default=8080)),
                ('env', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='env.environ')),
                ('envproc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.projectprocess')),
            ],
        ),
    ]
