# Create your views here.
from rest_framework import mixins, viewsets

from api.serializers import TagSerializer
from recipes.models import Tag


class TagApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
