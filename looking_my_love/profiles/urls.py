from django.urls import path
from .views import *

urlpatterns = [
    path('api/list', UserListView.as_view()),
    path('api/clients/create', UserCreateView.as_view()),
    path('api/clients/<int:pk>/match', MatchCreateView.as_view())
]