from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Job
from .forms import JobForm


# 列出所有職缺
class IndexView(ListView):
    template_name = "jobs/index.html"
    model = Job
    context_object_name = "jobs"


# 新增職缺
class AddView(CreateView):
    template_name = "jobs/create.html"
    model = Job
    form_class = JobForm
    success_url = reverse_lazy("jobs:index")


class ShowView(DetailView):
    model = Job
    context_object_name = "job"
    template_name = "jobs/show.html"
