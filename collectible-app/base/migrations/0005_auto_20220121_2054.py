# Generated by Django 2.1.15 on 2022-01-21 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='floor_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]