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



class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = "/users/"
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)

class UserHomeView(TemplateView):
    template_name = 'users/home.html'

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

