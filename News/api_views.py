from rest_framework import viewsets
from .serializers import ArticleSerializer, CommentSerializer
from .models import Article, Comment


class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
