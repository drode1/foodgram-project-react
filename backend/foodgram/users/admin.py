from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Класс для управления пользователями в админке сайта. """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email',)
    list_filter = ('username', 'email',)
