# Generated by Django 3.2 on 2021-04-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_task_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Заголовок'),
        ),
    ]
