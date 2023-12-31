import os

from django.db.models import Sum

from openpyxl import Workbook

from foodgram_backend import settings
from recipes.models import ProductsInRecipe


def status_check(request, serializable_object, model):
    """Проверка наличия запрашиваемого объекта в БД."""
    return (
        request.user.is_authenticated
        and model.objects.filter(
            recipe=serializable_object.pk,
            user=request.user.pk,
        ).exists()
    )


def adding_ingredients(instance, ingredients):
    """Добавление ингредиентов к рецепту при создании и обновлении."""
    for ingredient in ingredients:
        ProductsInRecipe.objects.create(
            recipe=instance,
            ingredient=ingredient.get('id'),
            amount=ingredient.get('amount'),
        )


def preparing_data_for_sending(request):
    """Подготовка данных для отправки списка покупок пользователю."""
    ingredient_data = []
    file_name = os.path.join(
        settings.BASE_DIR,
        'recipes',
        request.user.username + '_ingredients.xlsx',
    )
    ingredients = (
        ProductsInRecipe.objects.filter(
            recipe__shoppinglists__user=request.user
        )
        .values(
            'ingredient__name',
            'ingredient__measurement_unit',
        )
        .order_by(
            'ingredient__name',
        )
        .annotate(
            amount=Sum('amount'),
        )
    )
    for ingredient in ingredients:
        (*data,) = ingredient.values()
        ingredient_data.append(data)
    shopping_cart = Workbook()
    list = shopping_cart.active
    list.append(
        (
            'Название ингредиента',
            'Единица измерения',
            'Количество в рецепте',
        )
    )
    for ingredient in ingredient_data:
        list.append(ingredient)
    shopping_cart.save(file_name)
    return file_name


def check_repetitions(value):
    """Поиск повторений тегов и ингредиентов в рецепте."""
    return {field for field in value if value.count(field) > 1}


def check_subscribed(request, model, obj):
    """Проверка подписки."""
    return (
        request.user.is_authenticated
        and model.objects.filter(
            author=obj.pk,
            user=request.user.pk,
        ).exists()
    )
