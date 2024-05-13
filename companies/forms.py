# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Company
from django import forms

class CompanyUserCreationForm(forms.Form):

    class Meta:
        model = Company
        fields = ['username', 'email', 'company_name', 'tin', 'user_name', 'tel']

class CompanyUserChangeForm(forms.Form):
    password = None
    
    class Meta:
        model = Company
        fields = ['email', 'user_name', 'tel']

    