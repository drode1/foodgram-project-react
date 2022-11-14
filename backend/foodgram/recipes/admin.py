from django.contrib import admin

# Register your models here.
from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredientAmount,
                            RecipeTags
                            )

admin.site.register(Tag)
admin.site.register(Ingredient)


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
    list_display = ('name', 'author',)
    list_filter = ('name', 'author',)
