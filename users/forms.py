from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    
    username = forms.CharField(
        label="用戶名",
        help_text="20字或更少。僅限字母、數字和 @/./+/-/_ 符號。",
        error_messages={
            'unique': "此用戶名已存在。",
        }
    )
    email = forms.EmailField(
        label="電子郵件",
        error_messages={
            'unique': "此電子郵件已存在。",
        }
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(),
        help_text=(
            "您的密碼不能與您的其他個人資料過於相似。<br>"
            "您的密碼必須至少包含 8 個字。<br>"
            "您的密碼不能是常用密碼。<br>"
            "您的密碼不能全為數字。<br>"
        )
    )
    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(),
        help_text="請再次輸入密碼以確認。",
        error_messages={
            'password_mismatch': _("兩次輸入的密碼不同。")
        }
    )
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("兩次輸入的密碼不同。"),
                code='password_mismatch',
            )
        return password2

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
            })
    )
    password = forms.CharField(
        label='密碼',
        strip=False,
        widget=forms.PasswordInput()
    )
    
    error_messages = {
        'invalid_login': _(
            "請輸入正確的帳號和密碼。注意，帳號和密碼都區分大小寫。")
    }
    
