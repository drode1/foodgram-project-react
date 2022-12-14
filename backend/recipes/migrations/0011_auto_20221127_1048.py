# Generated by Django 3.2.16 on 2022-11-27 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0010_auto_20221126_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(blank=True, validators=[
                django.core.validators.MinValueValidator(1)],
                                                   verbose_name='Количество'),
        ),
    ]
