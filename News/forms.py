from django import forms
from .models import Article, Comment


# Форма для добавления новых статей
class PostNewArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Title', 'Content',)


# Форма для добавления комментариев
class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('Content',)
