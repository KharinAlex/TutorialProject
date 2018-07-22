from django.urls import path, include
from .api_views import UserView, UserProfileView


urlpatterns = [
    path('', UserView.as_view(), name='api_user'),
    path('profile/', UserProfileView.as_view(), name='api_profile'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]