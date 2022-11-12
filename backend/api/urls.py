from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
