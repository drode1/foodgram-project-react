from django.db.models import QuerySet, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import BaseGetApiView
from api.permissions import IsUserOrAdminOrReadOnly
from api.serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                             ReadRecipeSerializer, RecipeSerializer,
                             SubscriptionSerializer, TagSerializer,
                             UserShoppingCartSerializer)
from recipes.models import (FavoriteRecipes, Ingredient, Recipe,
                            RecipeIngredientAmount, Tag, UserShoppingCart)
from users.models import Subscription, User


class TagApiView(BaseGetApiView):
    """ Класс для обработки тегов. """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientApiView(BaseGetApiView):
    """ Класс для обработки ингредиентов. """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вью для обратки рецептов. """

    queryset = Recipe.objects.all()
    permission_classes = (IsUserOrAdminOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)

    @staticmethod
    def add_action_method(request, pk: int, serializers, instance) -> Response:
        """
        Общий метод для обработки запросов на добавление подписки и товаров
        в корзину.
        """

        data = {'user': request.user.id, 'recipe': pk}
        instance = instance.objects.filter(user_id=request.user.id,
                                           recipe_id=pk).exists()
        if instance:
            return Response({'errors': 'Такой объект уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_action_method(request, pk: int, instance) -> Response:
        """
        Общий метод для обработки запросов на удаление подписок и товаров
        в корзине.
        """

        get_object_or_404(instance, user=request.user, recipe__id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=('POST',),
            permission_classes=(permissions.IsAuthenticated,),
            url_path=r'(?P<pk>\d+)/favorite')
    def favorite(self, request, pk: int) -> Response:
        """ Метод для добавления рецептов в избранное. """

        return self.add_action_method(request, pk, FavoriteRecipeSerializer,
                                      FavoriteRecipes)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk: int) -> Response:
        """ Метод для удаления рецептов из избранного. """

        return self.delete_action_method(request, pk, FavoriteRecipes)

    @action(detail=False, methods=('POST',),
            permission_classes=(permissions.IsAuthenticated,),
            url_path=r'(?P<pk>\d+)/shopping_cart')
    def shopping_cart(self, request, pk: int) -> Response:
        """ Метод для добавления товаров в корзину. """

        return self.add_action_method(request, pk, UserShoppingCartSerializer,
                                      UserShoppingCart)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk: int) -> Response:
        """ Метод для удаления товаров в корзине. """

        return self.delete_action_method(request, pk, UserShoppingCart)

    @action(detail=False, methods=('GET',),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request) -> HttpResponse:
        """ Метод для скачивания корзины ингредиентов пользователей. """

        cart_ingredient_amount = RecipeIngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user, ).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(ingredients_total=Sum('amount'))

        return self.generate_shopping_cart_file(cart_ingredient_amount)

    @staticmethod
    def generate_shopping_cart_file(queryset) -> HttpResponse:
        """
        Метод генерирует файл с ингредиентами на основе списка рецептов,
        которые пользователь добавил в корзину.
        """

        cart_ingredients = {}
        for ingredient in queryset:
            name = (f"{ingredient.get('ingredient__name')} "
                    f"({ingredient.get('ingredient__measurement_unit')})")
            amount = ingredient.get('ingredients_total')
            if name in cart_ingredients:
                cart_ingredients[name] += amount
            else:
                cart_ingredients[name] = amount

        response = HttpResponse(content_type='text/plain')
        file_body = 'Список покупок:\n'
        for name, amount in cart_ingredients.items():
            file_body += f'{name} – {amount} \n'
        response.write(file_body)
        return response


class SubscriptionApiView(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """ Вью выдачи списка подписок пользователя. """

    serializer_class = SubscriptionSerializer

    def get_queryset(self) -> QuerySet[User]:
        user = get_object_or_404(User, id=self.request.user.id)
        follower = Subscription.objects.filter(user=user).values('follower')
        return User.objects.filter(id__in=follower)


class SubscribeApiView(APIView):
    """ Вью для обработки подписок и удаления подписок у пользователей. """

    permission_classes = (IsUserOrAdminOrReadOnly,)
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs) -> Response:
        user = request.user
        follower_id = self.kwargs.get('user_id')
        if user.id == follower_id:
            return Response({'error': 'Нельзя подписаться на себя'},
                            status=status.HTTP_400_BAD_REQUEST)

        if Subscription.objects.filter(user=user,
                                       follower_id=follower_id).exists():
            return Response({'error': 'Вы уже подписаны на пользователя'},
                            status=status.HTTP_400_BAD_REQUEST)

        follower = get_object_or_404(User, id=follower_id)
        Subscription.objects.create(user=user, follower_id=follower_id)
        return Response(
            self.serializer_class(follower, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs) -> Response:
        get_object_or_404(Subscription, user=request.user,
                          follower_id=self.kwargs.get('user_id')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
