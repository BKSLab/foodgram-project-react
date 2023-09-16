from django.contrib import admin

from .models import User


class BaseAdmin(admin.ModelAdmin):
    '''Общий класс для регистрации моделей.'''

    empty_value_display = '-пусто-'


@admin.register(User)
class UserAdmin(BaseAdmin):
    '''Регистрация модели пользователей.'''

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = ('username', 'email')
    search_fields = ('username__startswith',)
