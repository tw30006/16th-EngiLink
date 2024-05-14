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

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        self.success_url = f"/companies/{pk}/jobs/" 
        return super().form_valid(form)



class ShowView(DetailView):
    template_name = "jobs/show.html"
    model = Job
    context_object_name = "job"


class EditView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/edit.html"
    context_object_name = "job"

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        self.success_url = f"/companies/{pk}/jobs/" 
        return super().form_valid(form)


class JobDeleteView(DeleteView):
    model = Job
    success_url = "companies/<pk>/jobs"

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        self.success_url = f"/companies/{pk}/jobs/" 
        return super().form_valid(form)