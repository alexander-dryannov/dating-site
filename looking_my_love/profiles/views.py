from .serializers import UsersListSerializer, UsersCreateSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FormParser, MultiPartParser
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from sys import getsizeof
from pathlib import Path
from .models import User
from uuid import uuid4
from io import BytesIO
from PIL import Image


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    # permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersCreateSerializer
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
                                        field_name="avatar",
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
