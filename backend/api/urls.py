from django.urls import include, path
from rest_framework import routers

from api.views import TagApiView, IngredientApiView, RecipeViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagApiView, basename='tags')
router.register(r'ingredients', IngredientApiView, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path(r'', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
