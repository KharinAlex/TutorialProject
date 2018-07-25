from django.urls import path, include
from .api_views import ArticleView, CommentView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('articles', ArticleView)
router.register('comments', CommentView)

urlpatterns = [
    path('auth', include('rest_framework.urls', namespace="news_api")),
    path('', include(router.urls)),
]