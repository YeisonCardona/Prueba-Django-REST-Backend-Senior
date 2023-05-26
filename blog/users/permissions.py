from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


########################################################################
class IsAdmin(permissions.BasePermission):
    """
    Solo los administradores y superusuarios pueden realizar todas las operaciones.
    Los usuarios autenticados pueden realizar operaciones de lectura.
    Los usuarios anónimos no tienen acceso.
    """

    # ----------------------------------------------------------------------
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        elif request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        else:  # POST, PUT, PATCH, DELETE
            return bool(request.user and (request.user.is_superuser or request.user.role == 'admin'))


########################################################################
class IsEditor(permissions.BasePermission):
    """
    Los editores pueden realizar todas las operaciones.
    Los usuarios autenticados pueden realizar operaciones de lectura.
    Los usuarios anónimos no tienen acceso.
    """

    # ----------------------------------------------------------------------
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        elif request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        else:  # POST, PUT, PATCH, DELETE
            return bool(request.user and (request.user.is_superuser or request.user.role in ['admin', 'editor']))


########################################################################
class IsBlogger(permissions.BasePermission):
    """
    Los bloggers solo pueden gestionar (leer, crear, actualizar, eliminar) sus propios posts, comentarios y likes.
    """

    # ----------------------------------------------------------------------
    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, AnonymousUser):
            return False
        elif request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        else:  # POST, PUT, PATCH, DELETE
            return bool(
                request.user and
                (request.user.is_superuser or request.user.role == 'blogger') and
                obj.author == request.user
            )
