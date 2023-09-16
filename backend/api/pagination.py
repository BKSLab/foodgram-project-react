from rest_framework import pagination


class RecipesPagination(pagination.PageNumberPagination):
    '''Пагинация для страницы рецептов'''

    page_size_query_param = 'limit'
