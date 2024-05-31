from django import forms
from .models import Resume
from datetime import date, datetime
import re
from django.core.exceptions import ValidationError


class EmailValidator(forms.EmailField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(self.email_regex_validator)

    def email_regex_validator(self, value):
        email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
            r")@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$",
            re.IGNORECASE,
        )

        if not email_re.match(value):
            raise ValidationError("請確認輸入的信箱!")
    
class ResumeForm(forms.ModelForm):

    email = EmailValidator()

    skills = forms.MultipleChoiceField(
        choices=Resume.SKILL_CHOICES, widget=forms.CheckboxSelectMultiple
    )
    birthday =  forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)

    picture = forms.ImageField(required=False)

    field_labels = {
        "name": "姓名",
        "gender": "性別",
        "phone_number": "手機",
        "address": "地址",
        "website": "個人網站",
        "experience": "工作經驗",
        "linkedin": "Linkedin",
        "github": "GitHub",
        "picture": "照片",
    }

    class Meta:
        model = Resume
        exclude = ["deleted_at", "created_at", "user", "posit"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        for field_name, label in self.field_labels.items():
            self.fields[field_name].label = label

        if request:
            full_name = f"{request.user.last_name}{request.user.first_name}"
            self.initial["name"] = full_name
            self.initial["email"] = request.user.email

    def clean_skills(self):
        return ", ".join(self.cleaned_data["skills"])

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not re.match(r"^[a-zA-Z\u4e00-\u9fa5\sａ-ｚＡ-Ｚ]+$", name):
            raise ValidationError("姓名不能有符號或數字!")
        return name
    
    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday:
            birthday = birthday.date() if isinstance(birthday, datetime) else birthday
            
            if birthday > date.today():
                raise ValidationError("請確認輸入的日期!")
            age = (
                date.today().year
                - birthday.year
                - (
                    (date.today().month, date.today().day)
                    < (birthday.month, birthday.day)
                )
            )
            if age < 16:
                raise ValidationError("請確認輸入的日期!")
        return birthday
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if len(phone_number) != 10 or not phone_number.startswith("09"):
            raise ValidationError("輸入格式錯誤, 電話必須是10碼並以09開頭!")
        return phone_number

    def clean_address(self):
        address = self.cleaned_data.get("address")

        if not re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9-]+$", address):
            raise ValidationError("請輸入正確格式!")
        if not re.search(r"[\u4e00-\u9fa5a-zA-Z]", address):
            raise ValidationError("請輸入正確格式!")
        if sum(num.isdigit() for num in address) > 10:
            raise ValidationError("請輸入正確格式!")
        if re.match(r"^[a-zA-Z0-9-]+$", address):
            raise ValidationError("請輸入正確格式!")
        
        return address
