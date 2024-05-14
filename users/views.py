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
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages


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

class UserPasswordChangeView(PasswordChangeView):
    template_name="users/password_change_form.html"
    success_url="/users/"

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'users/reset.html'  

    def form_valid(self, form):
        messages.success(self.request, 'A password reset link has been sent to your email.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to send password reset link. Please check the email address.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('users:password_reset_done')

class UserPasswordResetDoneView(PasswordResetDoneView):
    pass  

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')  

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been reset successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to reset password. Please try again.')
        return super().form_invalid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    pass  


