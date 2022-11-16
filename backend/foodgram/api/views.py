from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter
from api.permissions import IsUserOrAdminOrReadOnly, IsOwner
from api.serializers import (TagSerializer, IngredientSerializer,
                             RecipeSerializer, ReadRecipeSerializer,
                             SubscriptionSerializer)
from recipes.models import Tag, Ingredient, Recipe
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
