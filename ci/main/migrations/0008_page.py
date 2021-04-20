# Generated by Django 3.2 on 2021-04-20 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_task_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=250, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='Title')),
                ('alias', models.CharField(max_length=50, verbose_name='Alias')),
                ('content', models.CharField(max_length=250, verbose_name='Content')),
                ('content_ru', models.CharField(max_length=250, null=True, verbose_name='Content')),
                ('content_en', models.CharField(max_length=250, null=True, verbose_name='Content')),
            ],
        ),
    ]
