from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializerLogin, UserSerializerAccount
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


class AccountsView(CreateAPIView):
    queryset = User.objects.none()
    serializer_class = UserSerializerAccount


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializerLogin(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
