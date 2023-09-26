from django.db import transaction
from django.db.models import F

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.utils import adding_ingredients, check_repetitions, status_check
from recipes.models import (
    Favorites,
    Ingredient,
    ProductsInRecipe,
    Recipe,
    ShoppingList,
    Tag,
)
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов в рецепте."""

    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для обработки GET запросов к рецептам."""

    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        """Получение игредиента в рецепте."""
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('productsinrecipe_recipe__amount'),
        )

    def get_is_in_shopping_cart(self, obj):
        """Обработка поля, отвечающего за добавление рецепта в корзину."""
        return status_check(self.context.get('request'), obj, ShoppingList)

    def get_is_favorited(self, obj):
        """Обработка поля, отвечающего за добавление рецепта в избранное."""
        return status_check(self.context.get('request'), obj, Favorites)


class ProductsInRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для колличества ингредиентов в рецепте."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = ProductsInRecipe
        fields = (
            'id',
            'amount',
        )

    def validate_amount(self, value):
        """Валидация поля amount."""
        if value <= 0:
            raise serializers.ValidationError(
                'Нужно указать количество ингредиента в рецепте'
            )
        return value


class CreateUpdateDeleteRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания, изменения и удаления рецептов."""

    ingredients = ProductsInRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )
        extra_kwargs = {
            'cooking_time': {'required': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецептов."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data)
        adding_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        """Изменение выходных данных сериализатора."""
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            },
        ).data

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление рецептов."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        ProductsInRecipe.objects.filter(recipe=instance).delete()
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        instance.save()
        adding_ingredients(instance, ingredients)
        instance.tags.set(tags)
        return instance

    def validate_tags(self, value):
        """Валидация поля tags."""
        if len(value) == 0:
            raise serializers.ValidationError(
                'Создать рецепт без указания хотя бы одного тега нельзя.'
            )
        if check_repetitions(value):
            raise serializers.ValidationError(
                'Повторение тегов не допускается.'
            )
        return value

    def validate_ingredients(self, value):
        """Валидация поля ingredients."""
        if len(value) == 0:
            raise serializers.ValidationError(
                'Создать рецепт без ингредиентов нельзя'
            )
        if check_repetitions([ingredient.get('id') for ingredient in value]):
            raise serializers.ValidationError(
                [
                    'Повторение ингредиентов не доступно.'
                ]
            )
        return value

    def validate_cooking_time(self, value):
        """Валидация поля cooking_time."""
        if value <= 0:
            raise serializers.ValidationError(
                'Время приготовления рецепта не может быть равным 0'
            )
        return value


class FavoritesSerializer(serializers.ModelSerializer):
    """Сериалайзер для избранного."""

    class Meta:
        model = Favorites
        fields = ('recipe', 'user')


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка покупок."""

    class Meta:
        model = ShoppingList
        fields = ('recipe', 'user')


class FavoriteAndShoppingListRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для избранного и списка покупок в рецепте."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'cooking_time',
        )
