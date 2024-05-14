from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser

class CompanyRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CompanyRegisterForm, self).__init__(*args, **kwargs)
        self.initial['user_type'] = 2  # Automatically set user_type for 'company'

    def save(self, commit=True):
        user = super(CompanyRegisterForm, self).save(commit=False)
        user.user_type = 2  # Set user_type for 'company'
        if commit:
            user.save()
        return user

class CompanyUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
