from celery.app.control import Control
from celery.result import AsyncResult
from celery_progress.views import get_progress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import *
from .models import *
from .tasks import *
from .utils import *

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
    {"models": list(ModelData.objects.all())},
]


class ProgressRecorder:
    def __init__(self, request, task_id):
        self.current_task = AsyncResult(task_id)
        self.request = request

    def set_progress(self, progress_percentage):
        self.current_task.task_meta["progress"] = progress_percentage
        self.current_task.save()

    def get_progress(self, request):  # updated method
        task = self.current_task
        if task.state == "PENDING":
            return 0
        elif task.state != "FAILURE":
            progress = task.info.get("progress", 0)
            return progress
        else:
            return 100


class AddRequest(FormView):
    form_class = AddRequestDataForm
    template_name = "search/addrequest.html"
    slug_url_kwarg = "model_slug"
    success_url = reverse_lazy("model_set")

    def dispatch(self, request, *args, **kwargs):
        self.request.session["task_id"] = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление запроса"
        context["models"] = list(ModelData.objects.all())
        context["menu"] = menu
        task_id = self.request.session.get("task_id")
        print(f"Celery Task ID: {task_id}")
        if task_id:
            task = AsyncResult(task_id)
            print(f"The task state is: {task.state}")  # will be set to PROGRESS_STATE
            print(f"The task info is: {task.info}")  # metadata will be here
            context["task"] = task
            progress_recorder = ProgressRecorder(self.request, task_id)
            job_progress = progress_recorder.get_progress(self.request)
            print("Progress is", job_progress)
            context["job_progress"] = job_progress
        return context

    def form_valid(self, form):
        text = form.cleaned_data.get("request_text")
        n_images = form.cleaned_data.get("num_samples")
        a = RequestData.objects.create(
            request_text=text, num_samples=n_images, slug=uuid.uuid4().hex, time_create=timezone.now()
        )
        a.save()
        task = get_images_fit_request.delay(a.id, text, n_images)
        self.request.session["task_id"] = task.task_id
        print(f"Celery Task ID in form valid: {task.task_id}")
        ret_val = self.render_to_response(self.get_context_data(task_id=task.task_id))
        return super().form_valid(form)


class AddModel(CreateView):
    form_class = AddModelDataForm
    template_name = "search/addmodel.html"
    slug_url_kwarg = "model_slug"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление модели"
        context["menu"] = menu
        context["models"] = list(ModelData.objects.all())
        # print(self.kwargs["model_slug"])
        # a = ModelData.objects.last()
        # self.request_data = RequestData.objects.get(pk=self.kwargs["model_slug"])
        # a.save()
        # context["model_slug"] = self.kwargs["model_slug"]
        # print(self.request.session.get('model_data'))
        return context


class ModelInfo(DetailView):
    model = ModelData
    template_name = "search/model_info.html"
    slug_url_kwarg = "pk"
    context_object_name = "model_data"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "menu"
        context["models"] = list(ModelData.objects.all())
        context["menu"] = menu
        return context


class ImageListInfo(ListView):
    model = ImageData
    template_name = "search/image_data.html"
    context_object_name = "images"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "menu"
        context["menu"] = menu
        context["models"] = list(ModelData.objects.all())
        context["data"] = ImageData.objects.filter(request_data_id=self.kwargs["request_id"])
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
