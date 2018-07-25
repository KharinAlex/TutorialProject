from .models import Article, Comment
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('url', 'Title', 'Content', 'Date', 'Author')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'article_id', 'Content', 'Date', 'Author')
