from django.shortcuts import render, redirect
from django.views import View
from django.db.models import *
from django.db.models.functions import *
from datetime import *
from django.http import JsonResponse
from employee.forms import EmployeeForm

from .models import *



class EmployeeView(View):
    def get(self, request):
        employees = Employee.objects.all().order_by('hire_date')
        context = {"employees_list": employees}
        return render(request, "employee.html", context)

class PositionView(View):
    def get(self, request):
        positions = Position.objects.annotate(count = Count('employee__id')).order_by('id')
        context = {"positions_list": positions}
        return render(request, 'position.html', context)
    
class ProjectView(View):
    def get(self, request):
        projects = Project.objects.all().order_by('id')
        context = {"projects_list": projects}
        return render(request, "project.html", context)
    
    def delete(self, request, project_id):
        project = Project.objects.get(id = project_id)
        res = {
            "message" : f"Deleted Project {project.name}"
        }
        project.delete()
        return JsonResponse(res, status=200)
    
    
class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id = project_id)
        project.start_date = project.start_date.strftime("%Y-%m-%d")
        project.due_date = project.due_date.strftime("%Y-%m-%d")
        context = {"project":project}
        return render(request, 'project_detail.html', context)
    
    def put(self, request, project_id, employee_id):
        project = Project.objects.get(id = project_id)
        employee = Employee.objects.get(id = employee_id)
        project.staff.add(employee)
        res = {
            "message" : f"Added staff {employee.get_full_name}"
        }
        return JsonResponse(res, status=200)
        
    def delete(self, request, project_id, employee_id):
        project = Project.objects.get(id = project_id)
        employee = Employee.objects.get(id = employee_id)
        project.staff.remove(employee)
        res = {
            "message" : f"Removed staff {employee.get_full_name}"
        }
        return JsonResponse(res, status=200)
    
class IndexView(View):
    def get(self, request):
        return redirect("employees")
    
class LayoutView(View):
    def get(self, request):
        return render(request, 'layout.html')
    
class EmployeeFormView(View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, "employee_form.html", {"form":form})
    
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid() :
            pass
        else:
            return render(request, "employee_form.html", {"form":form})
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        gender = form.cleaned_data["gender"]
        birth_date = form.cleaned_data["birth_date"]
        hire_date = form.cleaned_data["hire_date"]
        salary = form.cleaned_data["salary"]
        position = form.cleaned_data["position"]
        
        emp = Employee(
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            birth_date = birth_date,
            hire_date = hire_date,
            salary = salary,
            position = position
        )
        emp.save()
        return redirect("employees")