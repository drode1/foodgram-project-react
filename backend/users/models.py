from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('Имя',
                                  max_length=settings.DEFAULT_USER_MAX_LENGTH)
    last_name = models.CharField('Фамилия',
                                 max_length=settings.DEFAULT_USER_MAX_LENGTH)
    email = models.EmailField('Почта',
                              max_length=settings.DEFAULT_EMAIL_MAX_LENGTH,
                              validators=[EmailValidator])
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-date_joined', 'username')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='follower', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, verbose_name='Подписчик',
                                 related_name='following',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'follower'],
                name='Unique follow required',

            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.follower.username}'
