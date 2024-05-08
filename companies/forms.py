from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Company

class CompanyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CompanyUserCreationForm, self).__init__(*args, **kwargs)
        if self.data:
            self.fields['password1'].widget.attrs['value'] = self.data.get('password1', '')
            self.fields['password2'].widget.attrs['value'] = self.data.get('password2', '')

    class Meta(UserCreationForm.Meta):
        model = Company
        fields = ['username', 'email', 'company_name', 'tin', 'user_name', 'tel']

class CompanyUserChangeForm(UserChangeForm):
    password = None
    
    class Meta(UserChangeForm.Meta):
        model = Company
        fields = ['email', 'user_name', 'tel']

    