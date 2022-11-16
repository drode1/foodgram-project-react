from rest_framework import filters


class IngredientFilter(filters.SearchFilter):
    """ Фильтр по строке без учета регистра. """

    search_param = 'name'
