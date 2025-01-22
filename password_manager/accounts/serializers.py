from rest_framework import serializers
from .models import Accounts


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Accounts
        fields = ['id', 'email', 'service_name', 'user', 'password']

        extra_kwargs = {
            'user': {'read_only': True}
        }

        def create(self, validated_data):
            """ Creates a new account with hashed password """
            password = validated_data.pop('password', None)
            account = Accounts(**validated_data)
            if password:
                account.password = password
            account.save()
            return account

        def update(self, instance, validated_data):
            """ Updates an existing account with hashed password """
            password = validated_data.pop('password', None)
            instance = super().update(instance, validated_data)
            if password:
                instance.password = password
            instance.save()
            return instance


class DecryptPasswordSerializer(serializers.Serializer):
    master_password = serializers.CharField(write_only=True)
    decrypted_password = serializers.CharField(read_only=True)

    class Meta:
        fields = ['master_password']