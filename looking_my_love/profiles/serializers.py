from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'avatar')


class UsersCreateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(allow_empty_file=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'email', 'avatar', 'password',)

    def create(self, validated_data):
        user = super(UsersCreateSerializer, self).create(validated_data)
        user.set_password(make_password(validated_data['password']))
        user.save()
        return user
