from rest_framework import permissions, viewsets


class BaseGetApiView(viewsets.ReadOnlyModelViewSet):
    """ Базовый класс используемый для тегов и ингредиентов. """

    permission_classes = (permissions.AllowAny,)
    pagination_class = None
