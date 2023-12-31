# Generated by Django 4.1.5 on 2023-01-26 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RequestData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "request_text",
                    models.CharField(max_length=255, verbose_name="Текст запроса"),
                ),
                (
                    "num_samples",
                    models.IntegerField(verbose_name="Колличество картинок"),
                ),
                ("slug", models.SlugField(max_length=255, verbose_name="URL")),
                (
                    "time_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Публикация"),
                ),
            ],
            options={
                "verbose_name": "Запрос",
                "verbose_name_plural": "Запросы",
                "ordering": ["-time_create", "request_text"],
            },
        ),
        migrations.CreateModel(
            name="ModelData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=100, verbose_name="Тип модели")),
                (
                    "model_data",
                    models.JSONField(null=True, verbose_name="Данные модели"),
                ),
                ("slug", models.SlugField(max_length=255, verbose_name="URL")),
                (
                    "request_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="search.requestdata",
                        verbose_name="Запрос",
                    ),
                ),
            ],
            options={
                "verbose_name": "Модель",
                "verbose_name_plural": "Модели",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ImageData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        height_field=480,
                        upload_to="photos/%Y/%m/%d/",
                        verbose_name="Фото",
                        width_field=480,
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("slug", models.SlugField(max_length=255, verbose_name="URL")),
                (
                    "request_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="search.requestdata",
                        verbose_name="Запрос",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение",
                "verbose_name_plural": "Изображения",
                "ordering": ["id"],
            },
        ),
    ]
