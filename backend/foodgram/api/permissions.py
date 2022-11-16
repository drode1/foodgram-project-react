from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    """ Права для проверки, является ли пользователь владельцем объекта """

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.followwewr


class IsUserOrAdminOrReadOnly(permissions.BasePermission):
    """ Права для проверки является пользователь владельцем объекта. """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return request.user

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.username == obj.author or request.user.is_staff
