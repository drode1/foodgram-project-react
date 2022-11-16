from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    """ Права для проверки, является ли пользователь владельцем объекта """

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.followwewr


class IsUserOrAdminOrReadOnly(permissions.IsAuthenticated):
    """ Права для проверки является пользователь владельцем объекта. """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return request.user

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.author or request.user.is_staff
