from django_filters import rest_framework
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientsFilter(rest_framework.FilterSet):
    """Фильтрация ингредиентов."""

    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    """Фильтрация рецептов."""

    author = filters.CharFilter(field_name='author__id')
    # tags = rest_framework.AllValuesMultipleFilter(
    #     queryset=Tag.objects.all(),
    #     field_name='tags__slug',
    #     to_field_name='slug',
    # )
    # AllValuesMultipleFilter(field_name='tags__slug')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='check_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='check_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def check_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def check_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shoppinglists__user=self.request.user)
        return queryset
