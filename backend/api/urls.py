from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

v1_urlpatterns = (
    [
        path('', include(router_v1.urls)),
    ],
    'v1'
)

auth_patterns = (
    [
        path('auth/', include('djoser.urls.authtoken')),
    ],
    'auth'
)

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
    path('v1/', include(auth_patterns)),
]
