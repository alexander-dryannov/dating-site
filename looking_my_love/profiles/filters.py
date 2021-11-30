from django_filters import rest_framework as filters
from .models import User


class UserListFilter(filters.FilterSet):
    gender = filters.CharFilter(field_name='gender')
    fname = filters.CharFilter(field_name='first_name')
    lname = filters.CharFilter(field_name='last_name')

    class Meta:
        model: User
        fields: ['fname', 'lname', 'gender']