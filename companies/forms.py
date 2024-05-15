from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser
from .models import Company

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
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("信箱已被人註冊")
        return email

class CompanyUpdateForm(UserChangeForm):
    company_name = forms.CharField(max_length=100)
    tin = forms.CharField(max_length=8)
    user_name = forms.CharField(max_length=100)
    tel = forms.CharField(max_length=11)

    class Meta:
        model = CustomUser
        fields = ['username', 'email','company_name','tin','user_name','tel']
    

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']

        self.fields['username'].label = '帳號'
        self.fields['email'].label = '公司信箱'
        self.fields['company_name'].label = '公司名稱'
        self.fields['tin'].label = '統一編號'
        self.fields['user_name'].label = '聯絡人'
        self.fields['tel'].label = '聯絡電話'

        if 'instance' in kwargs:
            user = kwargs['instance']
            company = getattr(user, 'company', None)
            if company:
                self.fields['company_name'].initial = company.company_name
                self.fields['tin'].initial = company.tin
                self.fields['user_name'].initial = company.user_name
                self.fields['tel'].initial = company.tel


    def save(self, commit=True):
        user = super().save(commit=False)
        if user.user_type == 2:
            company, created = Company.objects.update_or_create(
            custom_user=user, 
            defaults={
                'company_name': self.cleaned_data["company_name"],
                'tin': self.cleaned_data["tin"],
                'user_name': self.cleaned_data["user_name"],
                'tel': self.cleaned_data["tel"]
                }
            )
            if commit:
                company.save()
        if commit:
            user.save()
        return user
    
