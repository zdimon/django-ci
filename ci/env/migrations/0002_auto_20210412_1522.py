# Generated by Django 3.2 on 2021-04-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='environprocess',
            name='path',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Каталог'),
        ),
        migrations.AlterField(
            model_name='environprocess',
            name='command',
            field=models.CharField(default='', max_length=250, verbose_name='Комманда'),
        ),
    ]
