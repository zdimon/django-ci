# Generated by Django 3.2 on 2021-04-15 11:43

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_commit_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='desc',
            field=tinymce.models.HTMLField(),
        ),
    ]
