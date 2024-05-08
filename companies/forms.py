from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Company

class CompanyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Company
        fields = ['username', 'email', 'company_name', 'tin', 'user_name', 'tel']

class CompanyUserChangeForm(UserChangeForm):
    password = None
    
    class Meta(UserChangeForm.Meta):
        model = Company
        fields = ['email', 'user_name', 'tel']

    