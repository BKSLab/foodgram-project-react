# Generated by Django 3.2.3 on 2023-09-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранные',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='название ингредиента'
                    ),
                ),
                (
                    'measurement_unit',
                    models.CharField(
                        max_length=200, verbose_name='единица измерения'
                    ),
                ),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='ProductsInRecipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.PositiveIntegerField(
                        verbose_name='количество ингредиента в рецепте'
                    ),
                ),
            ],
            options={
                'verbose_name': 'продукт в рецепте',
                'verbose_name_plural': 'продукты в рецепте',
                'ordering': ('recipe__name',),
                'default_related_name': 'productsinrecipe_recipe',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='название рецепта'
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        null=True,
                        upload_to='recipes/images/',
                        verbose_name='фотография',
                    ),
                ),
                ('text', models.TextField(verbose_name='описание')),
                (
                    'cooking_time',
                    models.PositiveIntegerField(
                        default=1,
                        verbose_name='время приготовления (в минутах)',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='дата и время публикации рецепта',
                    ),
                ),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'список покупок',
                'verbose_name_plural': 'списки покупок',
                'default_related_name': 'shoppinglists',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'подписчик',
                'verbose_name_plural': 'подписчики',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200,
                        unique=True,
                        verbose_name='название тега',
                    ),
                ),
                (
                    'color',
                    models.CharField(
                        max_length=7, unique=True, verbose_name='цвет в HEX'
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        max_length=200,
                        unique=True,
                        verbose_name='уникальный slug тега',
                    ),
                ),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
    ]
