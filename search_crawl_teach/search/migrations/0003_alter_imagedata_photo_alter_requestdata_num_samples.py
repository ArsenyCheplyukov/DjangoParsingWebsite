# Generated by Django 4.1.5 on 2023-02-03 21:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0002_alter_imagedata_photo_alter_modeldata_request_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagedata",
            name="photo",
            field=models.ImageField(upload_to="photos/", verbose_name="Фото"),
        ),
        migrations.AlterField(
            model_name="requestdata",
            name="num_samples",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(50),
                    django.core.validators.MaxValueValidator(500),
                ],
                verbose_name="Колличество картинок",
            ),
        ),
    ]
