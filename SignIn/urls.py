from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.LoginFormView.as_view()),
    path('', views.LoginFormView.as_view()),
    path('registration/', views.RegisterFormView.as_view()),
    path('logout/', views.LogoutView.as_view())
]