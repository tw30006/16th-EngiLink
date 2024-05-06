from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.views.generic import TemplateView, UpdateView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy


class UserIndexView(TemplateView):
    template_name = "users/index.html"


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
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Registration successfully, {name} Hello!")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please check your input.")
        return self.render_to_response(self.get_context_data(form=form))
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/edit.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("userindex")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Update completed!")
        return super().form_valid(form)

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'