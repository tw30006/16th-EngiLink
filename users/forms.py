from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields["password"]


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='帳號',
        max_length=20,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'input',
            })
    )
    password = forms.CharField(
        label='密碼',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        })
    )
    
    error_messages = {
        'invalid_login': _(
            "請輸入正確的帳號和密碼。注意，帳號和密碼都區分大小寫。")
    }
    
