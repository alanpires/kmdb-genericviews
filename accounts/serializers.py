from rest_framework import serializers
from .models import User


class UserSerializerAccount(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_superuser",
            "is_staff",
        ]

    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)


class UserSerializerLogin(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
