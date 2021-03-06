# Generated by Django 3.2 on 2021-04-20 09:12

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210420_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='desc_en',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='desc_ru',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='title_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='title_ru',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
