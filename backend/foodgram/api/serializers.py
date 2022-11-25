import base64
from typing import Dict

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from foodgram.recipes.models import (FavoriteRecipes, Ingredient, Recipe,
                                     RecipeIngredientAmount, RecipeTags, Tag,
                                     UserShoppingCart)
from foodgram.users.models import Subscription, User


class Base64ImageField(serializers.ImageField):
    """ Базовый класс для обработки файлов в base64 формате. """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format_type, img_string = data.split(';base64,')
            ext = format_type.split('/')[-1]
            data = ContentFile(base64.b64decode(img_string),
                               name='temp.' + ext
                               )

        return super().to_internal_value(data)


class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для создания пользователей. """

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Переопределяем метод, чтобы хэшировать пароль
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        user = User.objects.create(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для обработки пользователей. """

    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с такой почтой уже существует.')]
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj) -> bool:
        """
        Метод проверяющий подписан ли текущий пользователь на другого или
        нет пользователя.
        """

        username = self.context.get('request').user
        if username.is_anonymous or username == obj.username:
            return False
        return Subscription.objects.filter(user=username,
                                           follower_id=obj.id).exists()


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецептов, для вывода рецептов в подписках пользователей.
    """

    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = ('name', 'id', 'cooking_time',)


class SubscriptionSerializer(UserSerializer):
    """
    Сериализатор для обработки подписчиков, основанный на
    пользовательском сериализаторе.
    """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = ('username', 'first_name', 'last_name',)

    def get_recipes(self, obj) -> Dict:
        """ Метод для обработки лимита выдаваемых рецептов. """

        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        author = get_object_or_404(User, username=obj.username)
        recipes = Recipe.objects.filter(author=author)
        if limit:
            recipes = recipes.all()[:int(limit)]
        return RecipeListSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj) -> int:
        """
        Метод подсчитывающий кол-во рецептов, которые принадлежат одному
        пользователю.
        """

        recipe_author = get_object_or_404(User, username=obj.username)
        return Recipe.objects.filter(author=recipe_author).count()


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки тегов в рецептах. """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки ингредиентов. """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки ингредиентов в рецепте. """

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения краткой информации о рецепте.
    Используется в избранном и корзине.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class CreateRecipeIngredientAmountSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки ингредиентов при создании рецепта. """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'amount',)


class BaseRecipeSerializer(serializers.ModelSerializer):
    """ Базовый сериализатор для рецептов. """

    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart',)

    @staticmethod
    def check_object_exists(context, instance, obj):
        username = context.get('request').user
        if username.is_anonymous:
            return False
        return instance.objects.filter(user=username,
                                       recipe_id=obj.id).exists()

    def get_is_favorited(self, obj) -> bool:
        """
        Метод проверяющий добавил ли текущий пользователь рецепт в избранное.
        """

        return self.check_object_exists(self.context, FavoriteRecipes, obj)

    def get_is_in_shopping_cart(self, obj) -> bool:
        """
        Метод проверяющий добавил ли текущий пользователь рецепт в корзину.
        """

        return self.check_object_exists(self.context, UserShoppingCart, obj)


class RecipeSerializer(BaseRecipeSerializer):
    """ Сериализатор для обработки рецептов (создание, удаление, апдейт). """

    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all()
                                              )
    ingredients = CreateRecipeIngredientAmountSerializer(
        many=True,
        source='recipeingredientamount_set'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time',
        )

    def create(self, validated_data) -> object:
        ingredients = validated_data.pop('recipeingredientamount_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredient(ingredients, recipe)
        self.add_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data) -> object:
        instance.tags.clear()
        RecipeIngredientAmount.objects.filter(recipe=instance).delete()
        self.add_tags(validated_data.pop('tags'), instance)
        self.add_ingredient(validated_data.pop('recipeingredientamount_set'),
                            instance)
        return super().update(instance, validated_data)

    def validate(self, data):
        """ Валидируем теги и ингредиенты на пустые списки и дубликаты. """

        duplicate_error = serializers.ValidationError({
            'error': 'Нельзя добавить одинаковые элементы'
        })
        empty_error = serializers.ValidationError({
            'error': 'Список не может быть пустым'
        })
        ingredients_set = data['recipeingredientamount_set']
        if not ingredients_set:
            raise empty_error
        ingredients_list = []
        for ingredient in ingredients_set:
            if ingredient['id'] in ingredients_list:
                raise duplicate_error
            ingredients_list.append(ingredient['id'])
        tags = data['tags']
        if not tags:
            raise empty_error
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise duplicate_error
            tags_list.append(tag)
        return data

    @staticmethod
    def add_ingredient(ingredients, recipe) -> None:
        """ Метод для обработки массива ингредиентов. """

        for ingredient in ingredients:
            RecipeIngredientAmount.objects.create(
                ingredient=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount'),
            )
        return

    @staticmethod
    def add_tags(tags, recipe) -> None:
        """ Метод для обработки массива тегов. """

        for tag in tags:
            tag = Tag.objects.get(id=tag.id)
            RecipeTags.objects.create(tag=tag, recipe=recipe)
        return


class ReadRecipeSerializer(BaseRecipeSerializer):
    """ Сериализатор только для просмотра рецептов. """

    ingredients = RecipeIngredientAmountSerializer(
        many=True,
        source='recipeingredientamount_set',
    )
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time', 'is_favorited', 'is_in_shopping_cart',
        )


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки подписок пользователей на рецепты. """

    class Meta:
        model = FavoriteRecipes
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(instance.recipe, context=context).data


class UserShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки корзины пользователей. """

    class Meta:
        model = UserShoppingCart
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(instance.recipe, context=context).data
