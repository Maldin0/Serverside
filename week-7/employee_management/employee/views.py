from django.shortcuts import render, redirect
from django.views import View
from django.db.models import *
from django.db.models.functions import *
from datetime import *
from django.http import JsonResponse

from .models import *



class EmployeeView(View):
    def get(self, request):
        employees = Employee.objects.all().order_by('id')
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