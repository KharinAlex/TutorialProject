from django.db import models

class Article(models.Model):
    Title = models.CharField(max_length=150)
    Content = models.TextField()
    Date = models.DateTimeField()
    Author = models.CharField(max_length=60, default="")
# Create your models here.
