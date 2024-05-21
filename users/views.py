from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from companies.models import Company
from jobs.models import Job
from companies.models import Company


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = "/users/"
    
    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Welcome to EngiLink!'
        message = 'Thank you for registering on our site.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]  
        send_mail(subject, message, from_email, recipient_list)

class UserHomeView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        jobs = Job.objects.select_related('company').all()
        search_keyword = self.request.GET.get('q')
        if search_keyword:
            companies = Company.objects.filter(company_name__icontains=search_keyword)
        else:
            companies = Company.objects.all()
        context['companies'] = companies
        context['jobs'] = jobs
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
    template_name = 'users/login.html'
    def get_success_url(self):
        return reverse_lazy('users:home')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/detail.html'
    context_object_name = 'user'
    login_url = "/users/"

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=1)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = "/users/"
    login_url = "/users/"

    def get_queryset(self):
        return CustomUser.objects.filter(user_type=1, id=self.request.user.id)

class UserPasswordChangeView(PasswordChangeView):
    template_name="users/password_change_form.html"
    success_url="/users/"

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response
