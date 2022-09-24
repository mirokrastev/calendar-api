from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_password(self, value):
        if not validate_password(value):
            return value

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
