# Generated by Django 3.2 on 2021-04-20 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Account'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='card',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Card number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='desc',
            field=models.TextField(blank=True, max_length=25, null=True, verbose_name='Tech'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_photo/%Y/%m/%d/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='telegram',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='telegram'),
        ),
    ]
