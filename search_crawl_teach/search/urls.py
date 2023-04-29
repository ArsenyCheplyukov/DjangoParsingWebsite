from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", AddRequest.as_view(), name="home"),
    path("model/", AddModel.as_view(), name="model_set"),
    path("model_validation/<int:pk>", ModelInfo.as_view(), name="validation"),
    path("images/<int:request_id>", ImageListInfo.as_view(), name="image_show"),
    # path("task-status/", AddRequest.as_view(), name="task_status"), # <uuid:task_id>
    # path("celery-progress/<uuid:task_id>", include("celery_progress.urls")),
]
