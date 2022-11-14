from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    email = models.EmailField('Почта', max_length=255,
                              validators=[EmailValidator]
                              )
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-date_joined', 'username')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
