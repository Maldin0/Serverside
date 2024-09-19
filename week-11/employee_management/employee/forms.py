from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import *
import datetime
from django.core.exceptions import ValidationError
from company.models import *

class EmployeeForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={"cols": 30, "rows": 3}))
    district = forms.CharField(max_length=100)
    province = forms.CharField(max_length=100)
    position = forms.ModelChoiceField(Position.objects.all())
    
    postal_code = forms.CharField(max_length=15)
    # print(Position.objects.get(id=1))

    class Meta:
        model = Employee
        fields = [
            "first_name", 
            "last_name", 
            "gender", 
            "birth_date", 
            "hire_date", 
            "salary", 
            "position",
            "location",
            "district",
            "province",
            "postal_code"
        ]
        widgets = {
            'birth_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
        
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "manager",
                  "due_date", "start_date", "staff"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}, 
                                          format='%Y-%m-%d'),
            "start_date": forms.DateInput(attrs={"type": "date"}, 
                                         format='%Y-%m-%d')
        }
    def clean_start_date(self):
        data = self.cleaned_data["start_date"]
        if data > datetime.date.today():
            raise ValidationError("Nuh uh")
        return data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].required = False
        
class ProjectDetailForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}, 
                                          format='%Y-%m-%d'),
            "start_date": forms.DateInput(attrs={"type": "date"}, 
                                         format='%Y-%m-%d')
        }
    def clean_start_date(self):
        data = self.cleaned_data["start_date"]
        if data > datetime.date.today():
            raise ValidationError("Nuh uh")
        return data
            
        