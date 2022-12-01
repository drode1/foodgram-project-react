from django_filters import rest_framework

from recipes.models import Ingredient, Recipe


class IngredientFilter(rest_framework.FilterSet):
    """ Фильтр по строке без учета регистра. """

    name = rest_framework.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    """ Фильтр по нескольким параметрам в рецепте. """

    is_favorited = rest_framework.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='is_in_shopping_cart_filter')
    author = rest_framework.NumberFilter(field_name='author__id',
                                         lookup_expr='exact')
    tags = rest_framework.AllValuesMultipleFilter(field_name='tags__slug', )

    def is_favorited_filter(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
