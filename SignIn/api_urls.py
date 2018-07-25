from django.urls import path, include
from .api_views import UserView, UserProfileView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserView)
router.register('profile', UserProfileView)

urlpatterns = [
    path('auth', include('rest_framework.urls', namespace="profile_api")),
    path('', include(router.urls)),
]