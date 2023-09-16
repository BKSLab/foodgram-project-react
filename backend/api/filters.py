from django_filters import rest_framework

from recipes.models import Ingredient, Recipe


class IngredientsFilter(rest_framework.FilterSet):
    '''Фильтрация ингредиентов.'''

    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    '''Фильтрация рецептов.'''

    author = rest_framework.CharFilter(field_name='author__id')
    tags = rest_framework.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
