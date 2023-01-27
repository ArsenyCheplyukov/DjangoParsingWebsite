from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("", AddRequest.as_view(), name="home"),
    path("model/<int:model_slug>", AddModel.as_view(), name="model_set"),
    path("model_validation/<int:pk>", ModelInfo.as_view(), name="validation"),
]
