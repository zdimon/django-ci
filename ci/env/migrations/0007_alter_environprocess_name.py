# Generated by Django 3.2 on 2021-04-12 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env', '0006_alter_environprocess_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environprocess',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
    ]
