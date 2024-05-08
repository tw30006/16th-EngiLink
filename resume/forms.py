from django import forms
from .models import Profile,Education,Work,Project
from datetime import date

class ProfileForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(choices=Profile.SKILL_CHOICES, widget=forms.CheckboxSelectMultiple)
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1960, 2025)),
        initial=date(1990, 1, 15), 
        required=False
    )
    class Meta:
        model = Profile
        exclude = ['deleted_at','created_at']
    
    def clean_skills(self):
        return ', '.join(self.cleaned_data['skills'])

class EducationForm(forms.ModelForm):
    default_date = date(1990, 1, 15)
    date_widget = forms.SelectDateWidget(years=range(1960, 2025))  
    start_date = forms.DateField(
        widget=date_widget,
        initial=default_date,
        required=False
    )
    end_date = forms.DateField(
        widget=date_widget,
        initial=default_date,
        required=False
    )
    class Meta:
        model = Education
        exclude = ['deleted_at','created_at']

class WorkForm(forms.ModelForm):
    default_date = date(1990, 1, 15)
    date_widget = forms.SelectDateWidget(years=range(1960, 2025))  
    start_date = forms.DateField(
        widget=date_widget,
        initial=default_date,
        required=False
    )
    end_date = forms.DateField(
        widget=date_widget,
        initial=default_date,
        required=False
    )
    class Meta:
        model = Work
        exclude = ['deleted_at','created_at']

class ProjectForm(forms.ModelForm):
    technologies_used= forms.MultipleChoiceField(choices=Project.SKILL_CHOICES, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Project
        exclude = ['deleted_at','created_at']
        
    def clean_skills(self):
        return ', '.join(self.cleaned_data['technologies_used'])