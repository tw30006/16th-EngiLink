from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .forms import CustomLoginForm
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import UserRegisterForm, UserUpdateForm
from .models import CustomUser
from resumes.models import Resume 
from companies.models import Company
from companies.forms import CompanyUpdateForm

from jobs.models import Job, User_Job, Job_Resume
from mailchimp3 import MailChimp
from django.http import HttpResponseRedirect

from django.http import HttpResponse
from django.template.loader import render_to_string


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

class UserHomeView(PermissionRequiredMixin,TemplateView):
    template_name = 'users/home.html'
    permission_required = "user_can_show"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        resumes = Resume.objects.filter(user=self.request.user)
        jobs = Job.objects.select_related('company').all()
        search_keyword = self.request.GET.get('q')
        user_jobs = User_Job.objects.filter(user=self.request.user).values_list('job_id', flat=True)
        if search_keyword:
            companies = Company.objects.filter(company_name__icontains=search_keyword)
            jobs = Job.objects.filter(title__icontains=search_keyword).select_related('company')
            company_ids_from_jobs = jobs.values_list('company_id', flat=True)
            companies_from_jobs = Company.objects.filter(id__in=company_ids_from_jobs)
            companies = companies | companies_from_jobs
            companies = companies.distinct()
        else:
            companies = Company.objects.all()
            jobs = Job.objects.select_related('company').all()
        context['companies'] = companies
        context['jobs'] = jobs
        context['resumes'] = resumes
        context['user_jobs'] = user_jobs
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
    form_class = CustomLoginForm
    
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


class UserPasswordChangeView(PermissionRequiredMixin,PasswordChangeView):
    template_name = "users/password_change_form.html"
    success_url = "/users/"
    permission_required = "user_can_show"

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:login'))
        return super().handle_no_permission() 
    
    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response

class UserAddView(LoginRequiredMixin,UpdateView):
    template_name = "users/create.html"
    model = Company
    form_class = CompanyUpdateForm
    success_url = "/companies/"
    login_url = "/companies/"

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "更新失敗")
        return super().form_invalid(form)

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    
class CollectJobView(LoginRequiredMixin, View):
    def post(self, request):
        job_id = request.POST.get("job_id")
        job = get_object_or_404(Job, id=job_id)
        user_job = User_Job.objects.filter(user=request.user, job=job)
        if user_job.exists():
            user_job.delete()
        else:
            user_job = User_Job.objects.create(job=job, user=request.user)
        
        if 'HX-Request' in request.headers:
            user_jobs = User_Job.objects.filter(user=request.user).values_list('job_id', flat=True)
            button_html = render_to_string('shared/collect_btn.html', {'job': job, 'user_jobs': user_jobs})
            return HttpResponse(button_html)
        return redirect("users:home")
    def get(self, request):
        jobs = Job.objects.select_related('company').all()
        user_jobs = User_Job.objects.filter(user=request.user).values_list('job_id', flat=True)
        return render(request, "users/collect.html", {'jobs': jobs, 'user_jobs': user_jobs})

@method_decorator(login_required, name='dispatch')
class ApplyForJobCreateView(View):
    def get(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        resumes = Resume.objects.filter(user=request.user)
        return render(request, 'jobs/apply.html', {'job': job, 'resumes': resumes})
    
    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        resume_id = request.POST.get('resume_id')               
        Job_Resume.objects.create(job_id=job_id, resume_id=resume_id, status='applied')
        return redirect('users:home')

class ApplyForJobListView(ListView):
    model = Job_Resume
    template_name = 'users/apply.html'
    def get_queryset(self):
        return Job_Resume.objects.filter(resume__user=self.request.user)

@method_decorator(login_required, name='dispatch')
class WithdrawApplicationView(View):
    def post(self, request, *args, **kwargs):
        job_resume_id = self.kwargs.get('pk')
        job_resume = get_object_or_404(Job_Resume, pk=job_resume_id, resume__user=request.user)
        job_resume.status = 'withdrawn'
        job_resume.withdrawn_at = timezone.now()
        job_resume.save()
        return redirect('users:home')

@method_decorator(login_required, name='dispatch')
class InterviewResponseView(View):
    def post(self, request, *args, **kwargs):
        job_resume_id = self.kwargs.get('pk')
        response = request.POST.get('response')
        job_resume = get_object_or_404(Job_Resume, pk=job_resume_id, resume__user=request.user)
        
        if response == 'accept':
            job_resume.accepted = 'accept'
        elif response == 'reject':
            job_resume.accepted = 'reject'
        
        job_resume.save()
        
        return redirect('users:home')