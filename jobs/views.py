from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Job
from .forms import JobForm


class IndexView(ListView):
    template_name = "jobs/index.html"
    model = Job
    context_object_name = "jobs"


class AddView(CreateView):
    template_name = "jobs/create.html"
    model = Job
    form_class = JobForm
    success_url = reverse_lazy("jobs:index")


class ShowView(DetailView):
    model = Job
    context_object_name = "job"
    template_name = "jobs/show.html"


class EditView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/edit.html"
    context_object_name = "job"
    success_url = reverse_lazy("jobs:index")


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("jobs:index")
