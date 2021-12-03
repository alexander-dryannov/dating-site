from django_filters import rest_framework as filters
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from fake_useragent import UserAgent
from .models import User


def handler_distance(current_user_address, another_user_address):
    ua = UserAgent()
    geolocator = Nominatim(user_agent=ua.random)
    current_user_location = geolocator.geocode(current_user_address)
    another_user_location = geolocator.geocode(another_user_address)
    return great_circle(
        (current_user_location.latitude, current_user_location.longitude),
        (another_user_location.latitude, another_user_location.longitude)
    ).km


class UserListFilterGeo(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        new_queryset = []
        users = queryset
        parameter_distance = request.GET.get('distance')
        if parameter_distance and bool(int(parameter_distance)):
            for user in users:
                current_user_address = f'{request.user.city}, {request.user.street}'
                another_user_address = f'{user.city}, {user.street}'
                distance = handler_distance(current_user_address, another_user_address)
                if distance <= float(parameter_distance):
                    new_queryset.append(user)
            return new_queryset
        return queryset


class UserListFilter(filters.FilterSet):
    gender = filters.CharFilter(field_name='gender')
    first_name = filters.CharFilter(field_name='first_name')
    last_name = filters.CharFilter(field_name='last_name')
    city = filters.CharFilter(field_name='city')

    class Meta:
        model: User
