from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram_backend import settings


class User(AbstractUser):
    """Модель для работы с пользователями."""

    username = models.CharField(
        'уникальный юзернейм',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'адрес электронной почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    password = models.CharField(max_length=150)
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    def __str__(self) -> str:
        return self.username[: settings.SHOW_CHARACTERS]
