from rest_framework import serializers
from .models import Accounts


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id', 'email', 'service_name', 'user']

        extra_kwargs = {
            'password_hash': {'write_only': True},
            'user': {'read_only': True}
        }

        def create(self, validated_data):
            """ Creates a new account with hashed password """
            password = validated_data.pop('password_hash', None)
            account = Accounts(**validated_data)
            if password:
                account.set_password(password)
            account.save()
            return account

        def update(self, instance, validated_data):
            """ Updates an existing account with hashed password """
            password = validated_data.pop('password_hash', None)
            instance = super().update(instance, validated_data)
            if password:
                instance.set_password(password)
            instance.save()
            return instance


class DecryptPasswordSerializer(serializers.Serializer):
    master_password = serializers.CharField(write_only=True)
    decrypted_password = serializers.CharField(read_only=True)