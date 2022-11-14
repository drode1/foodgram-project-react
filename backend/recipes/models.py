from django.core.validators import RegexValidator
from django.db import models


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
