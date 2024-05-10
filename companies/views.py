from .forms import CompanyUserCreationForm, CompanyUserChangeForm
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company

class LogOutView(LogoutView):
    template_name = "companies/logout.html"


class LogInView(LoginView):
    template_name = "companies/login.html"

    def get_success_url(self):
        url = self.get_redirect_url()
        return reverse("index") 

class IndexView(TemplateView):
    template_name = "companies/index.html"
    context_object_name = 'user'


class SignUpView(CreateView):
    form_class = CompanyUserCreationForm
    model = Company
    template_name = "companies/signup.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response
    

class UpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyUserChangeForm
    template_name = "companies/update.html"
    success_url = reverse_lazy("index")
    
    def get_object(self):
        return self.request.user

class ShowView(LoginRequiredMixin, DetailView):
    model = Company
    form_class = CompanyUserChangeForm
    template_name = 'companies/show.html'
    context_object_name = 'user'