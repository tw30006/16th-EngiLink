from django.contrib import messages
from django.contrib.auth import logout, login, get_backends
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from users.models import CustomUser
from .models import Company
from jobs.models import Job_Resume
from .forms import CompanyRegisterForm, CompanyUpdateForm 
from django.http import HttpResponseRedirect, HttpResponseForbidden
import rules


def get_user_backend(user):
    for backend in get_backends():
        if backend.get_user(user.pk) is not None:
            return backend
    raise Exception("No backend found for user")


class CompanyRegisterView(FormView):
    template_name = "companies/register.html"
    form_class = CompanyRegisterForm

    def form_valid(self, form):
        user = form.save()
        backend = get_user_backend(user)
        messages.success(self.request, "註冊成功")
        login(
            self.request,
            user,
            backend=backend.__module__ + "." + backend.__class__.__name__,
        )
        return super(CompanyRegisterView, self).form_valid(form)

    def get_success_url(self):
        user = self.request.user

        try:
            company = Company.objects.get(custom_user=user)
        except Company.DoesNotExist:
            company = None

        if user.user_type == 2 and company is None:
            return reverse_lazy('companies:update', kwargs={'pk': user.pk})
        else:
            return reverse_lazy('companies:home')


class CompanyHomeView(PermissionRequiredMixin,TemplateView):
    template_name = 'companies/home.html'
    permission_required = "company_can_show"



class CompanyLoginView(LoginView):
    template_name = 'companies/login.html'
    

    def get_default_redirect_url(self):
        user = self.request.user

        try:
            company = Company.objects.get(custom_user=user)
        except Company.DoesNotExist:
            company = None

        if user.user_type == 2 and company is None:
            return reverse_lazy('companies:update', kwargs={'pk': user.pk})
        else:
            return reverse_lazy('companies:home')


class CompanyLogoutView(PermissionRequiredMixin,LogoutView):
    next_page = reverse_lazy('home')
    permission_required = "company_can_show"

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "登出成功")
        return super().dispatch(request, *args, **kwargs)

class CompanyDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Company
    template_name = "companies/detail.html"
    context_object_name = "company"
    login_url = "/companies/"
    permission_required = "company_can_show"

    def dispatch(self, request, *args, **kwargs):
        self.company = self.get_object()
        if not rules.test_rule('is_current_company', request.user, self.company):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.custom_user
        return context

class CompanyUpdateView(PermissionRequiredMixin,LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "companies/update.html"
    context_object_name = "company"
    success_url = "/companies/"
    login_url = "/companies/"
    permission_required = "company_can_show"

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新失敗")
        return super().form_invalid(form)

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=2, id=self.request.user.id)


class CompanyPasswordChangeView(PermissionRequiredMixin,PasswordChangeView):
    template_name="companies/password_change_form.html"
    success_url="/companies/"
    permission_required = "company_can_show"

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('companies:login'))
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        response = super().form_valid(form)
        logout(self.request)
        return response

class CompanyListView(ListView):
    model = Company
    template_name = 'companies/list.html'
    context_object_name = 'companies_list' 

    def get_queryset(self):
        queryset = Company.objects.all()
        search_keyword = self.request.GET.get("q")
        if search_keyword:
            queryset = queryset.filter(company_name__icontains=search_keyword)
        return queryset

    
class JobApplicationsView(ListView):
    model = Job_Resume
    template_name = 'companies/apply.html'
    def get_queryset(self):
        company = get_object_or_404(Company, custom_user=self.request.user)
        return Job_Resume.objects.filter(job__company=company)

class JobApplicationDetailView(DetailView):
    model = Job_Resume
    template_name = 'companies/candidate.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        resume = user.resume
        context['resume'] = resume
        context['educations'] = resume.educations.all()
        context['works'] = resume.works.all()
        context['projects'] = resume.projects.all()
        return context

class MarkAsReadView(View):
    def post(self, request, *args, **kwargs):
        job_resume_id = self.kwargs.get('pk')
        job_resume = get_object_or_404(Job_Resume, id=job_resume_id)
        if request.user == job_resume.job.company.custom_user:
            job_resume.read_at = timezone.now()
            job_resume.save()
        return redirect('companies:applications', pk=job_resume.job.company_id)