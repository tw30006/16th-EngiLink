from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CompanyUserCreationForm, CompanyUserChangeForm
from .models import Company

class CompanyUserAdmin(UserAdmin):
    add_form = CompanyUserCreationForm
    form = CompanyUserChangeForm
    model = Company
    list_display = ['username', 'email', 'company_name', 'tin', 'user_name', 'tel']

admin.site.register(Company, CompanyUserAdmin)
