import json

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy

# TYPE WE CHOOSE FROM THIS LIST:
TYPES = [
    ("1", "Option 1"),
    ("2", "Option 2"),
    ("3", "Option 3"),
    ("4", "Option 4"),
]


class RequestData(models.Model):
    request_text = models.CharField(max_length=255, verbose_name="Текст запроса")
    num_samples = models.IntegerField(
        verbose_name="Колличество картинок", validators=[MinValueValidator(10), MaxValueValidator(500)]
    )
    slug = models.SlugField(max_length=255, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return self.request_text[:25]

    def get_absolute_url(self):
        # return reverse_lazy("model_set", kwargs={"model_slug": self.id})
        return reverse_lazy("model_set")

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"
        ordering = ["-time_create", "request_text"]


class ImageData(models.Model):
    request_data = models.ForeignKey("RequestData", on_delete=models.CASCADE, verbose_name="Запрос")
    photo = models.ImageField(upload_to="photos/", verbose_name="Фото")
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="URL")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("model_set", kwargs={"model_slug": self.request_data})

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ["id"]


class ModelData(models.Model):
    request_data = models.ForeignKey(RequestData, default=True, on_delete=models.CASCADE, verbose_name="Запрос")
    type = models.CharField(max_length=1, null=False, choices=TYPES, verbose_name="Тип модели")
    model_data = models.JSONField(null=True, verbose_name="Данные модели")
    slug = models.SlugField(max_length=255, verbose_name="URL")

    def get_id(self):
        return self.id

    def __str__(self):
        return str(self.id) + ": " + self.type

    def get_absolute_url(self):
        return reverse_lazy("validation", kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"
        ordering = ["id"]
