from rest_framework import mixins, viewsets, permissions


class BaseGetApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ Базовый класс используемый для тегов и ингредиентов. """

    permission_classes = (permissions.AllowAny,)
    pagination_class = None
