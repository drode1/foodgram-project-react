from rest_framework import mixins, viewsets, filters

from api.serializers import TagSerializer, IngredientSerializer, \
    RecipeSerializer
from recipes.models import Tag, Ingredient, Recipe


class BaseGetApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ Базовый класс используемый для тегов и ингредиентов. """

    pagination_class = None


class TagApiView(BaseGetApiView):
    """ Класс для обработки тегов. """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientApiView(BaseGetApiView):
    """ Класс для обработки ингредиентов. """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # TODO: Сделать фильтрацию без регистра


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
