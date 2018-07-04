from django.urls import path
from django.views.generic import ListView
from . import views
from News.models import Article


urlpatterns = [
    path('', ListView.as_view(queryset=Article.objects.order_by("-Date")[:20],
                              template_name="News/news.html"), name='News_page'),
    path('new_post', views.post_new, name='new_post'),
    path('<pk>', views.post_detail, name='post_detail'),
    path('<pk>/comment', views.post_comment, name='post_comment'),
    path('comment/<pk>/edit', views.edit_comment, name='edit_comment'),
    path('comment/<pk>/delete', views.delete_comment, name='delete_comment'),
    path('<pk>/edit', views.post_edit, name='edit_post'),
    path('<pk>/delete', views.post_delete, name='delete_post'),
]
