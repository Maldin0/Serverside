# snippets/permissions.py

from rest_framework import permissions

class AppointmentListPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit and delete it.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "POST":
            return request.user.has_perm("appointments.add_appointment")
        elif request.method == "PATCH":
            return request.user.has_perm("appointments.change_appointment")
        elif request.method == "DELETE":
            return request.user.has_perm("appointment.delete_appointment")
        return False
    
class AppointmentDetailsPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit and delete it.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm("appointments.view_appointment")
        elif request.method == "POST":
            return request.user.has_perm("appointments.add_appointment")
        elif request.method == "PATCH":
            return request.user.has_perm("appointments.change_appointment")
        elif request.method == "DELETE":
            return request.user.has_perm("appointment.delete_appointment")
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return request.user.has_perm("appointments.change_appointment") and obj.created_by == request.user
        elif request.method == "DELETE":
            return request.user.has_perm("appointments.delete_appointment") and obj.created_by == request.user
        return False