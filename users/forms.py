from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import CustomUser
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=CustomUser.role_choice)
    
    class Meta:
        model = CustomUser
        fields = ["username", "email"]
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password1", "password2"]  
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
        return user