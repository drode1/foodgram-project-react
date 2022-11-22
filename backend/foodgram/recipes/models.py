from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """ Модель для тегов, используемых в рецептах. """

    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True,
                             null=True)
    slug = models.SlugField('Слаг', max_length=200, unique=True, null=True,
                            validators=[
                                RegexValidator(regex='[-a-zA-Z0-9_]+$')]
                            )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        db_table = 'tags'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Модель для ингредиентов, используемых в рецептах. """

    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        db_table = 'ingredients'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель рецептов. """

    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField('Время приготовления',
                                               validators=[
                                                   MinValueValidator(1)]
                                               )
    image = models.ImageField('Изображение',
                              upload_to='recipes/'
                              )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        verbose_name='Теги'
    )
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='author',
                               on_delete=models.CASCADE,
                               )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        db_table = 'recipes'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class RecipeIngredientAmount(models.Model):
    """ Пивот модель, используемая для хранения ингредиентов в рецепте. """

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               )
    amount = models.PositiveIntegerField('Количество',
                                         validators=[MinValueValidator(1)],
                                         blank=True,
                                         )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient} - {self.amount}'


class RecipeTags(models.Model):
    """ Пивот модель, используемая для хранения тегов в рецепте. """

    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name='Тег',
                            related_name='recipe_tag'
                            )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipe_tag'
                               )

    class Meta:
        verbose_name = 'Тег в рецептах'
        verbose_name_plural = 'Теги в рецептах'

    def __str__(self):
        return f'{self.recipe.name} - {self.tag}'


class FavoriteRecipes(models.Model):
    """ Модель подписок добавления рецептов в избранное у пользователей. """

    user = models.ForeignKey(User,
                             verbose_name='Подписчик',
                             on_delete=models.CASCADE,
                             related_name='favorite_recipe'
                             )
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='favorite_recipe'
                               )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        db_table = 'favorite'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Unique favorite required',

            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.recipe}'


class UserShoppingCart(models.Model):
    """ Модель корзины, куда пользователей может добавлять рецепты. """

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='shopping_cart'
                             )
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='shopping_cart'
                               )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        db_table = 'cart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Unique cart required',

            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.recipe}'
