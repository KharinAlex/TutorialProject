from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    Title = models.CharField(max_length=150)
    Content = models.TextField()
    Date = models.DateTimeField()
    Author = models.ForeignKey(User, on_delete=models)


class Comment(models.Model):
    class Meta:
        db_table = "Comments"
    article_id = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    Author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Date = models.DateTimeField()
    Content = models.TextField()
