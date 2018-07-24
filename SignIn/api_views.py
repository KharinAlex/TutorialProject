from rest_framework import viewsets
from django.contrib.auth.models import User
from SignIn import serializers, models


class UserView(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = serializers.UserSerializer


class UserProfileView(viewsets.ModelViewSet):
        queryset = models.UserModel.objects.all()
        serializer_class = serializers.UserProfileSerializer
