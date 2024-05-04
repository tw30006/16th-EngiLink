from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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


# 每一筆的詳細職缺內容
class ShowView(DetailView):
    model = Job
    context_object_name = "job"
    template_name = "jobs/show.html"


# 編輯
class EditView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/edit.html"
    context_object_name = "job"
    success_url = reverse_lazy("jobs:index")


# 軟刪除
class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("jobs:index")
