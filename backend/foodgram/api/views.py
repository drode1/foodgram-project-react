from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter
from api.permissions import IsUserOrAdminOrReadOnly, IsOwner
from api.serializers import (TagSerializer, IngredientSerializer,
                             RecipeSerializer, ReadRecipeSerializer,
                             SubscriptionSerializer, FavoriteRecipeSerializer,
                             UserShoppingCartSerializer)
from recipes.models import Tag, Ingredient, Recipe, FavoriteRecipes, \
    UserShoppingCart
from users.models import Subscription, User


class BaseGetApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ Базовый класс используемый для тегов и ингредиентов. """

    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class TagApiView(BaseGetApiView):
    """ Класс для обработки тегов. """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientApiView(BaseGetApiView):
    """ Класс для обработки ингредиентов. """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    # TODO: Сделать фильтрацию без регистра


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вью для обратки рецептов. """

    queryset = Recipe.objects.all()
    permission_classes = (IsUserOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def add_action_method(request, pk, serializers):
        # TODO: Передавать данные через получение объекта на проверку уникальности
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_action_method(request, pk, instance):
        recipe = get_object_or_404(Recipe, id=pk)
        instance = get_object_or_404(instance, user=request.user,
                                     recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=('POST', 'DELETE',),
            permission_classes=(permissions.IsAuthenticated,),
            url_path=r'(?P<pk>\d+)/favorite')
    def favorite(self, request, pk):
        """ Метод для добавления и удаления рецептов в избранное. """

        if request.method == 'POST':
            return self.add_action_method(request, pk,
                                          FavoriteRecipeSerializer)
        return self.delete_action_method(request, pk, FavoriteRecipes)

    @action(detail=False, methods=('POST', 'DELETE',),
            permission_classes=(permissions.IsAuthenticated,),
            url_path=r'(?P<pk>\d+)/shopping_cart')
    def shopping_cart(self, request, pk):
        """ Метод для добавления и удаления товаров в корзину. """

        if request.method == 'POST':
            return self.add_action_method(request, pk,
                                          UserShoppingCartSerializer)
        return self.delete_action_method(request, pk, UserShoppingCart)

    @action(detail=False, methods=('GET',),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        """ Метод для скачивания корзины пользователей. """

        return Response()


class SubscriptionApiView(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """ Вью выдачи списка подписок пользователя. """

    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        follower = Subscription.objects.filter(user=user).values('follower')
        query_set = User.objects.filter(id__in=follower)
        return query_set


class SubscribeApiView(APIView):
    """ Вью для обработки подписок и удаления подписок у пользователей. """

    permission_classes = (IsOwner,)
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
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

    def delete(self, request, *args, **kwargs):
        follower_id = self.kwargs.get('user_id')
        subscription = (
            Subscription.objects.filter(user=request.user,
                                        follower_id=follower_id)
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Вы не подписаны на пользователя'},
                        status=status.HTTP_400_BAD_REQUEST
                        )
