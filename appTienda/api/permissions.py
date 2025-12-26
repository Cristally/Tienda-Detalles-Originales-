from rest_framework import permissions
from django.contrib.auth.models import Group


class IsAdminUser(permissions.BasePermission):    
    message = "Solo los administradores pueden realizar esta acción."
    
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and (request.user.is_staff or 'Administrador' in request.user.groups.values_list('name', flat=True))
        )


class IsAdminOrReadOnly(permissions.BasePermission):    
    message = "Solo los administradores pueden modificar o eliminar datos."
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user 
            and request.user.is_authenticated 
            and (request.user.is_staff or 'Administrador' in request.user.groups.values_list('name', flat=True))
        )
