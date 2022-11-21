from django.urls import include, path
from rest_framework import routers

from api.views import (TagApiView, IngredientApiView, RecipeViewSet,
                       SubscriptionApiView, SubscribeApiView)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagApiView, basename='tags')
router.register(r'ingredients', IngredientApiView, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users/subscriptions', SubscriptionApiView,
                basename='subscriptions')

urlpatterns = [
    path('users/<int:user_id>/subscribe/', SubscribeApiView.as_view(),
         name='subscribe'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
