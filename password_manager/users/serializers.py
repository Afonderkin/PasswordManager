from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if 'username' not in validated_data or 'password' not in validated_data:
            raise serializers.ValidationError("Username and password are required.")

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()