from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir acceso si el usuario es un administrador o un superusuario
        return bool(request.user and (request.user.is_superuser or request.user.role == 'admin'))


class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir acceso si el usuario es un editor, administrador o superusuario
        return bool(request.user and (request.user.is_superuser or request.user.role in ['admin', 'editor']))


class IsBlogger(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permitir acceso si el usuario es un blogger, editor, administrador o superusuario y
        # si el objeto fue creado por el usuario actual
        return bool(
            request.user
            and (request.user.is_superuser or request.user.role in ['admin', 'editor', 'blogger'])
            and obj.author == request.user
        )
