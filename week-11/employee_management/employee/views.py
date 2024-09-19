from django.shortcuts import render, redirect
from django.views import View
from django.db.models import *
from django.db.models.functions import *
from datetime import *
from django.http import JsonResponse
from employee.forms import *
from django.forms.models import model_to_dict
from django.db import transaction
from .models import *
from company.models import *



class EmployeeView(View):
    def get(self, request):
        employees = Employee.objects.all().order_by('hire_date')
        for employee in employees:
            employee.position = Position.objects.get(pk=employee.position_id)
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
        form = ProjectDetailForm(instance=project)

        context = {
            "form" : form,
            "project" : project
        }
        return render(request, 'project_detail.html', context)
    
    def post(self, request, project_id):
        project = Project.objects.get(id= project_id)
        form = ProjectDetailForm(request.POST, instance=project)
        
        if form.is_valid() :
            pass
        else:
            return render(request, "project_detail.html", {"form":form})
        
        form.save()
        return redirect("projects_details", project_id=project_id)
    
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
    
    @transaction.atomic
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid() :
            pass
        else:
            return render(request, "employee_form.html", {"form":form})
        form = form.clean()
        
        with transaction.atomic():
            new_emp = Employee(
                first_name = form["first_name"],
                last_name = form["last_name"],
                gender = form["gender"],
                birth_date = form["birth_date"],
                hire_date = form["hire_date"],
                salary = form["salary"],
                position_id = form["position"].id
            )
            new_emp.save()
            addr = EmployeeAddress(
                employee = new_emp,
                location = form["location"],
                district = form["district"],
                province = form["district"],
                postal_code = form["postal_code"]
            )
            addr.save()
            # print(new_emp)
        return redirect("employees")

class ProjectFormView(View):
    def get(self, request):
        form = ProjectForm()
        return render(request, "project_form.html", {"form":form})
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect("projects")
        else:
            return render(request, "employee_form.html", {"form":form})
        
    