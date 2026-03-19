from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    """
    Permitir el acceso unicamente a los usuarios que tengan el rol de instructor
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.rol == 'instructor')