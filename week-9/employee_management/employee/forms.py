from django import forms
from .models import Position
from datetime import datetime

class EmployeeForm(forms.Form):
    GENDER_CHOICES = (
        ("M", 'Male'),
        ("F", 'Female'),
        ("LGBT", 'LGBT')
    )
    first_name = forms.CharField(max_length=155)
    last_name = forms.CharField(max_length=155)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, initial=0)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format='%Y-%m-%d'),
        input_formats=["%Y-%m-%d"]
        )
    hire_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format='%Y-%m-%d'),
        input_formats=["%Y-%m-%d"]
    )
    salary = forms.DecimalField(max_digits=10, decimal_places=2, initial=0)
    position = forms.ModelChoiceField(
        queryset=Position.objects.all()
    )