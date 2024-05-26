from django.contrib import messages
from django.contrib.auth import logout, login,authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm
from .models import CustomUser
from django.conf import settings
from companies.models import Company
from jobs.models import Job
from django.shortcuts import get_object_or_404, redirect, render
from jobs.models import User_Job
from django.views import View
from mailchimp3 import MailChimp



class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "註冊成功")
        self.add_user_to_mailchimp_list(user.email)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
        if user:
            login(self.request, user)
        
        return super().form_valid(form)

    def add_user_to_mailchimp_list(self, user_email):
        api_key = settings.MAILCHIMP_API_KEY
        list_id = settings.MAILCHIMP_LIST_ID
        client = MailChimp(mc_api=api_key)
        client.lists.members.create(list_id, {
            'email_address': user_email,
            'status': 'subscribed',
        })


class UserHomeView(TemplateView):
    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        jobs = Job.objects.select_related("company").all()
        user_jobs = User_Job.objects.filter(user=self.request.user).values_list('job_id', flat=True)
        search_keyword = self.request.GET.get("q")
                
        if search_keyword:
            companies = Company.objects.filter(company_name__icontains=search_keyword)
        else:
            companies = Company.objects.all()
        context["companies"] = companies
        context["jobs"] = jobs
        context["user_jobs"] = user_jobs
        return context

class UserJobsView(TemplateView):
    template_name = 'users/jobs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('jobs')
        if search_keyword:
            jobs = Job.objects.filter(title__icontains=search_keyword).select_related("company")
        else:
            jobs = Job.objects.select_related("company").all()
        context['jobs'] = jobs       
        return context


class UserLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, "登入成功")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "登入失敗")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("users:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "登出成功")
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/detail.html"
    context_object_name = "user"
    login_url = "/users/"

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=1)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = "/users/"
    login_url = "/users/"

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=1, id=self.request.user.id)

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        return super().form_valid(form)


class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change_form.html"
    success_url = "/users/"

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response

class CollectJobView(LoginRequiredMixin, View):
    def post(self, request):
        job_id = request.POST.get("job_id")
        job = get_object_or_404(Job, id=job_id)
        user_job = User_Job.objects.filter(user=request.user, job=job)
        if user_job.exists():
            user_job.delete()
        else:
            user_job = User_Job.objects.create(job=job, user=request.user)
        return redirect("users:home")

    def get(self, request):
        jobs = Job.objects.select_related('company').all()
        user_jobs = User_Job.objects.filter(user=request.user).values_list('job_id', flat=True)
        return render(request, "users/collect.html", {'jobs': jobs, 'user_jobs': user_jobs})
