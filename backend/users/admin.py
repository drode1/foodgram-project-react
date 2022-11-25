from django.contrib import admin

from recipes.models import Recipe
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Класс для управления пользователями в админке сайта. """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email',
                    'get_quantity_user_recipes',)
    list_filter = ('username', 'email',)

    @admin.display(description='Кол-во рецептов')
    def get_quantity_user_recipes(self, obj):
        """ Подсчитывает кол-во рецептов каждого пользователя. """

        return Recipe.objects.filter(author_id=obj.id).count()
