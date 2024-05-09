from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.views.generic import TemplateView, UpdateView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserIndexView(TemplateView):
    template_name = "users/index.html"


class SigninView(auth_views.LoginView):
    template_name = 'users/signin.html'
    
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or '/users/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST' and not self.request.POST.get('username') and not self.request.POST.get('password'):
            messages.info(self.request, "請輸入使用者代號與密碼!")
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "登入成功!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "登入失敗, 請確認輸入的訊息!")
        return self.render_to_response(self.get_context_data(form=form))

class SignoutView(SuccessMessageMixin, auth_views.LogoutView):
    template_name = 'users/signout.html'
    next_page = reverse_lazy('userindex')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "登出成功!")
        logout(request)  
        return super().dispatch(request, *args, **kwargs)

class SignupView(CreateView):
    model = User
    template_name = "users/signup.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('userindex')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        name = form.cleaned_data.get("username")
        user = authenticate(username=username, password=password)
        messages.success(self.request, "註冊成功!")
        if user is not None:
            login(self.request, user)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "註冊失敗, 請確認輸入的訊息!")
        return self.render_to_response(self.get_context_data(form=form))
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/edit.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("userindex")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "更新完成!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "更新失敗, 請確認輸入的訊息!")

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'