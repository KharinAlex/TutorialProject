from django.urls import path, include
from django.views.generic import ListView, DetailView
from News.models import Article


urlpatterns = [
    path('', ListView.as_view(queryset=Article.objects.order_by("-Date")[:20],
                              template_name="News/news.html")),
    path('<slug:pk>', DetailView.as_view(model=Article, template_name="News/post.html"))
]