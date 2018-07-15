from django.urls import path
from django.contrib.auth.models import User
from . import views


urlpatterns = [
    path('login/', views.LoginFormView.as_view()),
    path('profile/', views.ProfileView, name='Profile'),
    path('', views.LoginFormView.as_view()),
    path('registration/', views.RegisterFormView.as_view()),
    path('logout/', views.LogoutView.as_view())
]