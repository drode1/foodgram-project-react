from rest_framework import mixins, permissions, viewsets


class BaseGetApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ Базовый класс используемый для тегов и ингредиентов. """

    permission_classes = (permissions.AllowAny,)
    pagination_class = None
