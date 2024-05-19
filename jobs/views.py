from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import Job
from .forms import JobForm
from companies.models import Company
from django.urls import reverse
from companies.models import Company
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin


class IndexView(PermissionRequiredMixin,ListView):
    template_name = "jobs/index.html"
    model = Job
    context_object_name = "jobs"
    permission_required = "jobs.show_job"

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        company = get_object_or_404(Company, pk=pk)
        return Job.objects.filter(company=company)
    

class AddView(CreateView):
    template_name = "jobs/create.html"
    model = Job
    form_class = JobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        form.instance.company = get_object_or_404(Company, pk=self.kwargs.get('pk'))
        self.success_url = reverse('companies:jobs', kwargs={'pk': form.instance.company.pk})
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
    success_url = "companies/<pk>/jobs/"

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        self.success_url = f"/companies/{pk}/jobs/" 
        return super().form_valid(form)

class SetPublishView(DetailView):
    model=Job
    context_object_name = "job"

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.is_published = not self.object.is_published
        self.object.save()
        return render(request,"jobs/job.html",{"job":self.object})