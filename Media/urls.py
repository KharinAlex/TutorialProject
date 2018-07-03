from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="media_main"),
    path(r'image_upload', views.image_upload, name="image_upload"),
]