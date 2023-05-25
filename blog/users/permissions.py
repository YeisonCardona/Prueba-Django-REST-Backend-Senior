from rest_framework import permissions


########################################################################
class IsAdmin(permissions.BasePermission):

    # ----------------------------------------------------------------------
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'admin')


########################################################################
class IsEditor(permissions.BasePermission):

    # ----------------------------------------------------------------------
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in ['admin', 'editor'])


########################################################################
class IsBlogger(permissions.BasePermission):

    # ----------------------------------------------------------------------
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.role in ['admin', 'editor', 'blogger'] and
            obj.author == request.user
        )
