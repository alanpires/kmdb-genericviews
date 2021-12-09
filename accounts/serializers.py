from rest_framework import serializers
from .models import User


class UserSerializerAccount(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login', 'email', 'is_active', 'date_joined', 'groups', 'user_permissions']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializerLogin(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()
