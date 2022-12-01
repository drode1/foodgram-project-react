from rest_framework import permissions


class IsUserOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """ Права для проверки является пользователь владельцем объекта. """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
