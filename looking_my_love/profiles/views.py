from .serializers import UsersListSerializer, UserSerializer, MatchCreateSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FormParser, MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .filters import UserListFilter, UserListFilterGeo
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import User, Match
from sys import getsizeof
from pathlib import Path
from uuid import uuid4
from io import BytesIO
from PIL import Image


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    filter_backends = (DjangoFilterBackend, UserListFilterGeo)
    filterset_class = UserListFilter
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser, ]

    def create(self, request, *args, **kwargs):
        watermark_path = Path(__file__).resolve().parent.parent.joinpath('static/watermarks/watermark.png')
        if request.data.get('avatar'):
            img_io = BytesIO()
            img = Image.open(request.FILES['avatar'])
            watermark = Image.open(watermark_path)
            img.paste(watermark, (0, 0))
            img.save(img_io, format=img.format, optimize=True, progressive=True)
            img_io.seek(0)

            name = str(uuid4()) + "." + str(request.FILES['avatar']).split(".")[-1]
            content_type = request.data.get('avatar').content_type
            request.data['avatar'] = InMemoryUploadedFile(
                                        file=img_io,
                                        field_name='avatar',
                                        name=name,
                                        content_type=content_type,
                                        size=getsizeof(img_io),
                                        charset=None
                                    )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MatchCreateView(generics.CreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchCreateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_second = User.objects.get(pk=kwargs.get('pk'))
        for i in self.queryset.values('user', 'vote'):
            if i['user'] == kwargs.get('pk') and request.user.pk:
                message1 = (
                    'Вы понравились!',
                    f'Вы понравились {request.user.first_name} {request.user.last_name}',
                    settings.EMAIL_HOST_USER,
                    [user_second.email]
                )
                message2 = (
                    'Вы понравились!',
                    f'Вы понравились {user_second.first_name} {user_second.last_name}',
                    settings.EMAIL_HOST_USER,
                    [request.user.email]
                )
                send_mass_mail((message1, message2), fail_silently=False)
        request.data['user'] = request.user.pk
        request.data['vote'] = kwargs.get('pk')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
