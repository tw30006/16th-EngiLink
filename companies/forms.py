from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser
from .models import Company


class CompanyRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CompanyRegisterForm, self).__init__(*args, **kwargs)
        self.initial["user_type"] = 2

    def save(self, commit=True):
        user = super(CompanyRegisterForm, self).save(commit=False)
        user.user_type = 2
        if commit:
            user.save()
        return user


class CompanyUpdateForm(UserChangeForm):
    company_name = forms.CharField(max_length=100)
    tin = forms.CharField(max_length=8)
    user_name = forms.CharField(max_length=100)
    tel = forms.CharField(max_length=11)
    address = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    type = forms.CharField(max_length=50)
    banner = forms.ImageField(required=False)
    logo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "company_name", "tin", "user_name", "tel", "address", "description", "type", "banner", "logo"]

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        del self.fields["password"]

        self.fields["username"].label = "帳號"
        self.fields["email"].label = "公司信箱"
        self.fields["company_name"].label = "公司名稱"
        self.fields["tin"].label = "統一編號"
        self.fields["user_name"].label = "聯絡人"
        self.fields["tel"].label = "聯絡電話"
        self.fields["address"].label = "地址"
        self.fields["description"].label = "簡介"
        self.fields["type"].label = "類型"
        self.fields["banner"].label = "橫幅"
        self.fields["logo"].label = "Logo"

        if "instance" in kwargs:
            user = kwargs["instance"]
            company = getattr(user, "company", None)
            if company:
                self.fields["company_name"].initial = company.company_name
                self.fields["tin"].initial = company.tin
                self.fields["user_name"].initial = company.user_name
                self.fields["tel"].initial = company.tel
                self.fields["address"].initial = company.address
                self.fields["description"].initial = company.description
                self.fields["type"].initial = company.type
                self.fields["banner"].initial = company.banner
                self.fields["logo"].initial = company.logo

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.user_type == 2:
            company, created = Company.objects.update_or_create(
                custom_user=user,
                defaults={
                    "company_name": self.cleaned_data["company_name"],
                    "tin": self.cleaned_data["tin"],
                    "user_name": self.cleaned_data["user_name"],
                    "tel": self.cleaned_data["tel"],
                    "address": self.cleaned_data["address"],
                    "description": self.cleaned_data["description"],
                    "type": self.cleaned_data["type"],
                    "banner": self.cleaned_data["banner"],
                    "logo": self.cleaned_data["logo"],
                },
            )
            if commit:
                company.save()
        if commit:
            user.save()
        return user
