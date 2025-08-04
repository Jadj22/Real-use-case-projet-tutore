from django.urls import path, include
from rest_framework import routers
from .viewset import UserViewSet, UserRegisterViewSet, UserLoginViewSet, UserRefreshViewSet

router = routers.DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='auth-register')
router.register(r'login', UserLoginViewSet, basename='auth-login')
router.register(r'refresh', UserRefreshViewSet, basename='auth-refresh')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]