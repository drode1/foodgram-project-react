from django.contrib import admin
from recipes.models import (FavoriteRecipes, Ingredient, Recipe,
                            RecipeIngredientAmount, RecipeTags, Tag,
                            UserShoppingCart)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Класс для управления тегами в админке сайта. """

    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('name', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """ Класс для управления ингредиентами в админке сайта. """

    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)


class TagInline(admin.TabularInline):
    """ Вспомогательный класс для отображения тегов в модели рецептов. """

    model = RecipeTags
    extra = 2


class IngredientsInline(admin.TabularInline):
    """
    Вспомогательный класс для отображения ингредиентов в модели рецептов.
    """

    model = RecipeIngredientAmount
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Класс для управления рецептами в админке сайта. """

    inlines = (IngredientsInline, TagInline,)
    list_display = ('id', 'name', 'author',)
    list_filter = ('name', 'author',)


@admin.register(RecipeTags)
class RecipeTagsAdmin(admin.ModelAdmin):
    """ Класс для управления привязок тегов к рецептам в админке сайта. """

    list_display = ('id', 'tag', 'recipe',)
    list_filter = ('tag', 'recipe',)


@admin.register(FavoriteRecipes)
class FavoriteRecipesAdmin(admin.ModelAdmin):
    """ Класс для управления избранными рецептами в админке сайта. """

    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(UserShoppingCart)
class UserShoppingCartAdmin(admin.ModelAdmin):
    """ Класс для управления корзиной с рецептами в админке сайта. """

    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
