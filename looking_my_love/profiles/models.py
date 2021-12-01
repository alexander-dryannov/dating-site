from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [
        ('мужской', 'Я мужчина'),
        ('женский', 'Я женщина'),
    ]
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Электронная почта')
    avatar = models.ImageField('Аватар', upload_to='avatars')
    gender = models.CharField('Пол', max_length=10, choices=GENDER_CHOICES)
    latitude = models.DecimalField('Широта', max_digits=10, decimal_places=8)
    longitude = models.DecimalField('Широта', max_digits=10, decimal_places=8)
