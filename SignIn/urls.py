from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.LoginFormView.as_view(), name='Login'),
    path('profile/', views.ProfileView.as_view(), name='Profile'),
    path('profile/edit/', views.ProfileEdit.as_view(), name='ProfileEdit'),
    path('profile/user/edit/', views.UserEdit.as_view(), name='UserEdit'),
    path('profile/delete/', views.ProfileDelete.as_view(), name='ProfileDelete'),
    path('', views.LoginFormView.as_view()),
    path('registration/', views.RegisterFormView.as_view(), name='Registration'),
    path('logout/', views.LogoutView.as_view(), name='Logout'),
    path('api/', include('SignIn.api_urls')),
]
