# Generated by Django 3.2 on 2021-04-13 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env', '0006_auto_20210413_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environ',
            name='state',
            field=models.CharField(choices=[('clean', 'без изменений'), ('edited', 'есть правки')], default='clean', max_length=60, verbose_name='Состояние'),
        ),
    ]
