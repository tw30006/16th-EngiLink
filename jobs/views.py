from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import Job
from .forms import JobForm


# 列出所有職缺
class IndexView(TemplateView):
    template_name = "jobs/index.html"


# 新增職缺
class AddView(CreateView):
    template_name = "jobs/create.html"
    model = Job
    form_class = JobForm
    success_url = reverse_lazy("jobs:index")
