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
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=100)


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.ForeignKey(User, related_name='given_vote', on_delete=models.CASCADE)

    def __str__(self):
        if self.user.gender == 'мужской':
            return f"{self.user} понравилась {self.vote}"
        else:
            return f"{self.user} понравился {self.vote}"
