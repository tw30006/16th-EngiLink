from django import forms
from .models import Work
from datetime import date


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
