# Generated by Django 2.1.15 on 2022-01-22 10:24

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20220121_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='image',
            field=models.ImageField(null=True, upload_to=base.models.collection_image_file_path),
        ),
    ]