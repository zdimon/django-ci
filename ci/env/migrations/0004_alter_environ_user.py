# Generated by Django 3.2 on 2021-04-09 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210402_1621'),
        ('env', '0003_environ_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environ',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customer'),
        ),
    ]
