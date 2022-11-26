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
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Класс для управления рецептами в админке сайта. """

    inlines = (IngredientsInline, TagInline,)
    list_display = ('id', 'name', 'author', 'get_recipe_favorite_quantity',
                    'get_recipe_ingredients',)
    list_filter = ('name', 'author',)

    @staticmethod
    @admin.display(description='Лайки')
    def get_recipe_favorite_quantity(obj):
        """
        Метод подсчитывает пользователей добавили данный рецепт в избранное.
        """

        return FavoriteRecipes.objects.filter(recipe_id=obj.id).count()

    @staticmethod
    @admin.display(description='Ингредиенты')
    def get_recipe_ingredients(obj):
        """
        Метод выводит список ингредиентов, которые привязаны к рецепту.
        """

        return [ing for ing in Ingredient.objects.filter(recipe__id=obj.id)]


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
