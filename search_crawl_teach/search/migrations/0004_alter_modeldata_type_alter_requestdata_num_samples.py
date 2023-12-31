# Generated by Django 4.0 on 2023-05-02 14:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_alter_imagedata_photo_alter_requestdata_num_samples'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeldata',
            name='type',
            field=models.CharField(choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')], max_length=1, verbose_name='Тип модели'),
        ),
        migrations.AlterField(
            model_name='requestdata',
            name='num_samples',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(500)], verbose_name='Колличество картинок'),
        ),
    ]
