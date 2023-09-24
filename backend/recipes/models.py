from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

from foodgram_backend import settings
from users.models import User


class Tag(models.Model):
    """Модель для работы с тегами."""

    name = models.CharField(
        'название тега',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'цвет в HEX',
        validators=[
            validators.RegexValidator(
                regex=settings.PATTERN_HEX,
                message='Введенная строка не соответствует стандарту HEX.',
            ),
        ],
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'уникальный slug тега',
        validators=[
            validators.RegexValidator(
                regex=settings.PATTERN_SLUG,
                message='Использованы некорректные символы',
            ),
        ],
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def clean(self):
        if Tag.objects.filter(
            color=self.color.lower(),
        ).exists():
            raise ValidationError('Тег с таким цветом уже существует .')

    def save(self, *args, **kwargs):
        self.color = self.color.lower()
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name[: settings.SHOW_CHARACTERS]


class Ingredient(models.Model):
    """Модель для работы с ингредиентами."""

    name = models.CharField(
        'название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return (
            f'{self.name[: settings.SHOW_CHARACTERS]} '
            f'({self.measurement_unit})'
        )


class Recipe(models.Model):
    """Модель для работы с рецептами."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
        related_name='recipes',
    )
    name = models.CharField(
        'название рецепта',
        unique=True,
        max_length=200,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ProductsInRecipe',
        verbose_name='ингредиент',
        related_name='recipes',
    )
    image = models.ImageField(
        'фотография',
        upload_to='recipes/images/',
    )
    text = models.TextField('описание')
    cooking_time = models.PositiveSmallIntegerField(
        'время приготовления (в минутах)',
        validators=[
            validators.MaxValueValidator(
                1440,
                message='Так долго готовить нельзя.',
            ),
            validators.MinValueValidator(
                1,
                message='Рецепт требует, как минимум 1 минуты на готовку',
            ),
        ],
        default=1,
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='теги', related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'дата и время публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.name[: settings.SHOW_CHARACTERS]


class ProductsInRecipe(models.Model):
    """Модель для работы с ингредиентами в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'количество ингредиента в рецепте',
        validators=[
            validators.MaxValueValidator(
                message='Указано слишком большое количество ингредиента.',
                limit_value=100000,
            ),
            validators.MinValueValidator(
                message='Нужно указать количество ингредиента в рецепте.',
                limit_value=0,
            ),
        ],
    )

    class Meta:
        verbose_name = 'продукт в рецепте'
        verbose_name_plural = 'продукты в рецепте'
        default_related_name = 'productsinrecipe_recipe'
        ordering = ('recipe__name',)
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe',
            )
        ]

    def __str__(self) -> str:
        return f'Рецепт: {self.recipe.name[: settings.SHOW_CHARACTERS]}'


class BaseModelForShoppingListAndFavorites(models.Model):
    """Базовая модель для избранного и списка покупок."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe',
            )
        ]

    def __str__(self) -> str:
        return self.recipe.name[: settings.SHOW_CHARACTERS]


class ShoppingList(BaseModelForShoppingListAndFavorites):
    """Модель для работы со списком покупок."""

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        default_related_name = 'shoppinglists'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_user',
            )
        ]


class Favorites(BaseModelForShoppingListAndFavorites):
    """Модель для работы с избранным."""

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe',
            )
        ]


class Subscription(models.Model):
    '''Модель для работы с подписками.'''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_user_author'
            ),
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                'Пользователь не может подписаться сам на себя.'
            )

    def __str__(self) -> str:
        return self.author.username[: settings.SHOW_CHARACTERS]
