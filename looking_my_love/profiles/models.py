from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    ]
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField("Электронная почта")
    avatar = models.ImageField("Аватар", upload_to="avatars")
    gender = models.CharField("Пол", max_length=10, choices=GENDER_CHOICES)
