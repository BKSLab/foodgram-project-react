from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.utils import check_subscribed
from foodgram_backend import settings
from recipes.models import Recipe, Subscription
from users.models import User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериалайзер для регистрации пользователей."""

    username = serializers.RegexField(regex=settings.PATTERN, max_length=150)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'id',
            'password',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
                message='полня username и email должны быть уникальными',
            )
        ]


class CustomUserSerializer(UserSerializer):
    """Сериалайзер для работы с пользователями."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователя на автора рецепта."""
        return check_subscribed(
            self.context.get('request'),
            Subscription,
            obj,
        )


class SubscriptionsRecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для рецепта в подписках."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'cooking_time',
        )


class SubscriptionsSerializer(UserSerializer):
    """Сериалайзер для работы с подписками."""

    email = serializers.EmailField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователя на автора рецепта."""
        return check_subscribed(
            self.context.get('request'),
            Subscription,
            obj,
        )

    def get_recipes_count(self, obj):
        """Получение количество рецептов автора."""
        return Recipe.objects.filter(author__username=obj).count()

    def get_recipes(self, obj):
        """Получение рецептов автора."""
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit is None:
            return SubscriptionsRecipesSerializer(
                Recipe.objects.filter(author=obj.author),
                many=True,
            ).data
        return SubscriptionsRecipesSerializer(
            Recipe.objects.filter(author=obj.author)[: int(recipes_limit)],
            many=True,
        ).data
