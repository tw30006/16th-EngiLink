from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import Job
from .forms import JobForm
from companies.models import Company
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
import rules
from jobs.models import User_Job

class IndexView(PermissionRequiredMixin,ListView):
    template_name = "jobs/index.html"
    model = Job
    context_object_name = "jobs"
    permission_required = "jobs.show_job"

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        company = get_object_or_404(Company, pk=pk)
        if not rules.test_rule('is_current_company',request.user,company):
            return HttpResponseForbidden()
        return super().dispatch(request,*args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        company = get_object_or_404(Company, pk=pk)
        return Job.objects.filter(company=company)
        

class AddView(CreateView):
    template_name = "jobs/create.html"
    model = Job
    form_class = JobForm

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        company = get_object_or_404(Company, pk=pk)
        if not rules.test_rule('is_current_company',request.user,company):
            return HttpResponseForbidden()
        return super().dispatch(request,*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.company = get_object_or_404(Company, pk=self.kwargs.get("pk"))
        self.success_url = reverse(
            "companies:jobs", kwargs={"pk": form.instance.company.pk}
        )
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
        company_id = form.instance.company.id
        self.success_url = reverse('companies:jobs', kwargs={'pk': company_id})
        return super().form_valid(form)

class JobDeleteView(DeleteView):
    model = Job
    
    def get_success_url(self):
        pk = self.object.company.pk
        return reverse('companies:jobs', kwargs={'pk': pk})

class PublishView(DetailView):
    model=Job
    context_object_name = "job"
    template_name = "jobs/job.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_published = not self.object.is_published
        self.object.save()
        return render(request, "jobs/job.html", {"job":self.object})

class JobListView(ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_list = []
        for job in context['jobs']:
            company = job.company
            job_info = {
                'title': job.title,
                'company_name': company.company_name,
                'company_logo_url': company.logo.url if company.logo else '',
                'company_banner_url': company.banner.url if company.banner else '',
                'address': job.address,
                'salary': job.salary,
                'description': job.description,
                'id': job.id
            }
            job_list.append(job_info)
        context['jobs'] = job_list
        if self.request.user.is_authenticated:
            user_jobs = User_Job.objects.filter(user=self.request.user).values_list('job_id', flat=True)
            context['user_jobs'] = list(user_jobs)
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/detail.html'
    context_object_name = 'job'