from django.contrib import admin

from .models import (
    Favorites,
    Ingredient,
    ProductsInRecipe,
    Recipe,
    ShoppingList,
    Subscription,
    Tag,
)


class BaseAdmin(admin.ModelAdmin):
    """Общий класс для регистрации моделей."""

    empty_value_display = '-пусто-'


@admin.register(ProductsInRecipe)
class ProductsInRecipeAdmin(BaseAdmin):
    """Регистрация модели продуктов в рецепте."""

    list_display = (
        'ingredient',
        'amount',
    )


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    """Регистрация модели тегов."""

    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    """Регистрация модели ингредиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name__startswith',)


class RecipeInline(admin.TabularInline):
    """Отображение рецептов в админке."""

    model = Recipe.ingredients.through
    # extra = 1
    # min_num = 1


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    """Регистрация модели рецептов."""

    model = Recipe
    inlines = [
        RecipeInline,
    ]
    list_display = (
        'name',
        'author',
    )
    readonly_fields = ('count_favorites',)
    fields = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'tags',
        'count_favorites',
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name__startswith',)

    @admin.display(description='рецепт добавлен в избранное')
    def count_favorites(self, obj):
        """Количество рецептов, добавленных в избранное."""
        return obj.favorites.count()


@admin.register(Favorites)
class FavoritesAdmin(BaseAdmin):
    """Регистрация модели избранное."""

    list_display = ('recipe', 'user')


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    """Регистрация модели подписок на авторов."""

    list_display = ('user', 'author')


@admin.register(ShoppingList)
class ShoppingListAdmin(BaseAdmin):
    """Регистрация модели списка покупок."""

    list_display = (
        'recipe',
        'user',
    )
