from django.urls import path, include
from . import views
from .forms import PostNewArticle, PostComment
from .models import Article, Comment


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='News_page'),
    path('new_post', views.PostCreateView.as_view(model=Article, form_class=PostNewArticle), name='new_post'),
    path('<pk>', views.ArticleDetailView.as_view(), name='post_detail'),
    path('<pk>/comment', views.PostCreateView.as_view(model=Comment, form_class=PostComment), name='post_comment'),
    path('comment/<pk>/edit', views.PostEditView.as_view(model=Comment, form_class=PostComment), name='edit_comment'),
    path('comment/<pk>/delete', views.PostDeleteView.as_view(model=Comment), name='delete_comment'),
    path('<pk>/edit', views.PostEditView.as_view(model=Article, form_class=PostNewArticle), name='edit_post'),
    path('<pk>/delete', views.PostDeleteView.as_view(model=Article), name='delete_post'),
    path('api/', include('News.api_urls')),
]
