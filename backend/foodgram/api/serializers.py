from recipes.models import Tag, Ingredient, Recipe, RecipeIngredientAmount
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


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


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор используемый для обрабокти пользователей. """

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

    @staticmethod
    def get_is_subscribed(obj):
        # TODO: Убрать заглушку
        return False


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


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для обработки рецептов. """

    tags = TagSerializer(many=True, required=True)
    ingredients = RecipeIngredientAmountSerializer(
        many=True,
        source='recipeingredientamount_set'
    )
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time'
        )
