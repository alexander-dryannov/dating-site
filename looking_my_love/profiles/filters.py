from django_filters import rest_framework as filters
from geopy.distance import great_circle
from .models import User


def handler_distance(current_user_coord, another_user_coord):
    return great_circle(current_user_coord, another_user_coord).km


class UserListFilterGeo(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        new_queryset = []
        users = queryset
        parameter_distance = request.GET.get('distance')
        if parameter_distance and bool(int(parameter_distance)):
            for user in users:
                current_user_address = f'{request.user.city}, {request.user.street}'
                another_user_address = f'{user.city}, {user.street}'
                distance = handler_distance(
                    (request.user.latitude, request.user.longitude),
                    (user.latitude, user.longitude)
                )
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
