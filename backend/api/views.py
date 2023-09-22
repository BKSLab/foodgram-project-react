from django.http import FileResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientsFilter, RecipeFilter
from api.pagination import RecipesPagination
from api.permissions import ReadOrAddUpdateDelRecipePermissions
from api.serializers import (
    CreateUpdateDeleteRecipeSerializer,
    FavoriteAndShoppingListRecipeSerializer,
    FavoritesSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    ShoppingListSerializer,
    TagSerializer,
)
from api.utils import preparing_data_for_sending
from foodgram_backend import settings
from recipes.models import Favorites, Ingredient, Recipe, ShoppingList, Tag


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для получения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для получения ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    permission_classes = (ReadOrAddUpdateDelRecipePermissions,)
    pagination_class = RecipesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return CreateUpdateDeleteRecipeSerializer

    @action(
        detail=False,
        url_path=r'(?P<id>\d+)/favorite',
        methods=['post', 'delete'],
        serializer_class=FavoritesSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, *args, **kwargs):
        """Добавление и удаление рецепта из избранного."""
        recipe_id = kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        check_favorite = Favorites.objects.filter(
            recipe=recipe,
            user=user,
        ).exists()
        if request.method == 'POST':
            if not check_favorite:
                Favorites.objects.create(
                    recipe=recipe,
                    user=user,
                )
                serializer = FavoriteAndShoppingListRecipeSerializer(
                    instance=recipe
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в избранном.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == 'DELETE':
            if check_favorite:
                Favorites.objects.filter(
                    recipe=recipe,
                    user=user,
                ).delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Пользователь не добавлял рецепт в избранное'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        url_path=r'(?P<id>\d+)/shopping_cart',
        methods=['post', 'delete'],
        serializer_class=ShoppingListSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, *args, **kwargs):
        """Добавление и удаление рецепта из списка покупок."""
        recipe_id = kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        check_favorite = ShoppingList.objects.filter(
            recipe=recipe,
            user=user,
        ).exists()
        if request.method == 'POST':
            if not check_favorite:
                ShoppingList.objects.create(
                    recipe=recipe,
                    user=user,
                )
                serializer = FavoriteAndShoppingListRecipeSerializer(
                    instance=recipe
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == 'DELETE':
            if check_favorite:
                ShoppingList.objects.filter(
                    recipe=recipe,
                    user=user,
                ).delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Пользователь не добавил рецепт в список покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """Отправка списка покупок пользователю в формате xlsx."""
        file = preparing_data_for_sending(request)
        return FileResponse(
            open(file, 'rb'),
            content_type=settings.EXTENSION_MIME_TYPE_XLSX,
        )
