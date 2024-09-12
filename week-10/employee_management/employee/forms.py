from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import *
import datetime
from django.core.exceptions import ValidationError

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}, 
                                          format='%Y-%m-%d'),
            "hire_date": forms.DateInput(attrs={"type": "date"}, 
                                         format='%Y-%m-%d')
        }
    def clean_hire_date(self):
        data = self.cleaned_data["hire_date"]
        if data > datetime.date.today():
            raise ValidationError("Nuh uh")
        return data
        
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
            
        