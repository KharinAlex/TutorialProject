from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from SignIn import serializers, models


class UserView(APIView):

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class UserProfileView(APIView):

    def get(self, request):
        userModel = get_object_or_404(models.UserModel, user_id=request.user)
        serializer = serializers.UserProfileSerializer(userModel)
        return Response(serializer.data)
