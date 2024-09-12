from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("employees/", views.EmployeeView.as_view(), name="employees"),
    path("positions/", views.PositionView.as_view(), name='positions'),
    path("projects/", views.ProjectView.as_view(), name="projects"),
    path("projects/<int:project_id>/", views.ProjectDetailView.as_view(), name="projects_details"),
    path("projects/<int:project_id>/<int:employee_id>/", views.ProjectDetailView.as_view(), name="project_staff_manage"),
    path('projects/<int:project_id>/delete/', views.ProjectView.as_view(), name="project_delete"),
    path("layout/", views.LayoutView.as_view(), name="layout"),
    path("employees/add/", views.EmployeeFormView.as_view(), name="add_employees"),
    path("projects/new/", views.ProjectFormView.as_view(), name="new_project")
]
