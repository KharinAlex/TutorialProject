from django import forms
from .models import Article, Comment


class PostNewArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Title', 'Content',)


class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('Content',)
