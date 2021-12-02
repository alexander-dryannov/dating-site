from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Match

UserModel = get_user_model()


class MatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            gender=validated_data['gender'],
            avatar=validated_data['avatar'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'gender', 'password',)
