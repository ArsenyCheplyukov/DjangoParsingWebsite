from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("", AddRequest.as_view(), name="home"),
    path("model/", AddModel.as_view(), name="model_set"),
    path("model_validation/<int:pk>", ModelInfo.as_view(), name="validation"),
    path("images/<int:request_id>", ImageListInfo.as_view(), name="image_show")
]
