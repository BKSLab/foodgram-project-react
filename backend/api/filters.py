from django_filters import rest_framework

from recipes.models import Ingredient, Recipe


class IngredientsFilter(rest_framework.FilterSet):
    """Фильтрация ингредиентов."""

    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    """Фильтрация рецептов."""

    author = rest_framework.CharFilter(field_name='author__id')
    # tags = rest_framework.AllValuesMultipleFilter(
    #     queryset=Tag.objects.all(),
    #     field_name='tags__slug',
    #     to_field_name='slug',
    # )
    # AllValuesMultipleFilter(field_name='tags__slug')
    tags = rest_framework.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = rest_framework.BooleanFilter(method='check_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
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
