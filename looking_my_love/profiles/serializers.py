from django.contrib.auth import get_user_model
from rest_framework import serializers
from geopy.geocoders import Nominatim
from fake_useragent import UserAgent
from .models import User, Match

UserModel = get_user_model()


def get_coord(city, street):
    ua = UserAgent()
    geolocator = Nominatim(user_agent=ua.random)
    location = geolocator.geocode(f'{city}, {street}')
    return float(f'{location.latitude:.8f}'), float(f'{location.longitude:.8f}')


class MatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'city', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        lat, long = get_coord(validated_data['city'], validated_data['street'])
        user = UserModel.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            gender = validated_data['gender'],
            avatar = validated_data['avatar'],
            city = validated_data['city'],
            street = validated_data['street'],
            password = validated_data['password'],
            latitude = lat,
            longitude = long
        )
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'avatar', 'gender', 'city', 'street', 'password',)
