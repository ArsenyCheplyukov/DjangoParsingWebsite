from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import *
from .models import *
from .utils import *

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class AddRequest(CreateView):
    form_class = AddRequestDataForm
    template_name = "search/addrequest.html"
    slug_url_kwarg = "model_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление запроса"
        context["menu"] = menu
        return context

    # def get_queryset(self):
    #     return RequestData.objects.filter(is_published=True)


class AddModel(CreateView):
    form_class = AddModelDataForm
    template_name = "search/addmodel.html"
    slug_url_kwarg = "model_slug"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление модели"
        context["menu"] = menu
        # print(self.kwargs["model_slug"])
        # a = ModelData.objects.last()
        # self.request_data = RequestData.objects.get(pk=self.kwargs["model_slug"])
        # a.save()
        context["model_slug"] = self.kwargs["model_slug"]
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
        context["menu"] = menu
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
