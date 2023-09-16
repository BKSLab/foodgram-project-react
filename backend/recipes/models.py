from django.db import models

from users.models import User


class Tag(models.Model):
    '''Модель для работы с тегами.'''

    name = models.CharField(
        'название тега',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'цвет в HEX',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'уникальный slug тега',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    '''Модель для работы с ингредиентами.'''

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
        return f'{self.name} - {self.measurement_unit}'


class Recipe(models.Model):
    '''Модель для работы с рецептами.'''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
        related_name='recipes',
    )
    name = models.CharField(
        'название рецепта',
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
        null=True,
        default=None,
    )
    text = models.TextField('описание')
    cooking_time = models.PositiveIntegerField(
        'время приготовления (в минутах)',
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
        return self.name


class ProductsInRecipe(models.Model):
    '''Модель для работы с ингредиентами в рецепте.'''

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
    amount = models.PositiveIntegerField('количество ингредиента в рецепте')

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
        return f'{self.recipe}: {self.ingredient}'


class ShoppingList(models.Model):
    '''Модель для работы со списком покупок.'''

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
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        default_related_name = 'shoppinglists'

    def __str__(self) -> str:
        return self.recipe.name


class Favorites(models.Model):
    '''Модель для работы с избранным.'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_user_recipe'
            )
        ]

    def __str__(self) -> str:
        return self.recipe.name


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
            )
        ]

    def __str__(self) -> str:
        return self.author.username
