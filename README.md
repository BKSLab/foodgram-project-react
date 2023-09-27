# Проект Foodgram

## Foodgram - сервис для публикации пользователями рецептов своих любимых блюд.

После регистрации и авторизации пользователю Foodgram будет доступно:
- публикация своих рецептов;
- редактирование и удаление своих рецептов;
- просмотр профиля авторов рецептов;
- подписываться на любимых авторов рецептов;
- добавлять понравившиеся рецепты в избранное;
- на основе рецептов, добавленных в список покупок формировать список продуктов, необходимых для приготовления рецептов из списка покупок.

Если вы не авторизованный пользователь, голодным не останетесь. Для вас доступен просмотр всех опубликованных рецептов.

## Страницы проекта Foodgram

### Главная страница проекта: https://foodgram-bks.mooo.com
### Страница для администрирования проекта: https://foodgram-bks.mooo.com/admin/
### API проекта доступен по ссылке: https://foodgram-bks.mooo.com/api/
### Документация к API доступна по ссылке: https://foodgram-bks.mooo.com/api/docs/

## Варианты формирования запросов к API

### Регистрация пользователя на сайте

__Endpoint__: https://foodgram-bks.mooo.com/api/users/

__Права доступа__: доступно неавторизованным пользователлям

__Метод__: POST

__Пример запроса__:

    {
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123"
    }

__Пример ответа__:

    {
    "email": "vpupkin@yandex.ru",
    "id": 0,
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин"
    }

### Создание рецепта

__Endpoint__: https://foodgram-bks.mooo.com/api/recipes/

__Метод__: POST

__Права доступа__: доступно авторизованным пользователлям

__Пример запроса__:

    {
    "ingredients": [
        {
        "id": 1123,
        "amount": 10
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
    }

__Пример ответа__:

    {
    "id": 0,
    "tags": [
        {
        "id": 0,
        "name": "Завтрак",
        "color": "#E26C2D",
        "slug": "breakfast"
        }
    ],
    "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
    },
    "ingredients": [
        {
        "id": 0,
        "name": "Картофель отварной",
        "measurement_unit": "г",
        "amount": 1
        }
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "text": "string",
    "cooking_time": 1
    }

## Создание суперпользователя для работы с панелью администратора
После разворачивания проекта на сервере в Docker контейнерах, необходимо подключиться к контейнеру бэкенда 
и дать команду для создания суперпользователя.  
Сделать это можно следующей командой:

    sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser

После чего необходимо аккуратно ввести запрашиваемые данные. Обязательно создайте надежный и безопасный пароль

## Загрузка ингредиентов
Для того, чтобы пользователи могли создавать рецепты, необходимо выгрузить данные об ингредиентах в БД из подготовленного CSV файла.  
После того, как проект будет полностью запущен на сервере, введите следующую команду:

    sudo docker compose -f docker-compose.production.yml exec backend python manage.py load

## Об авторе
- Барабанщиков Кирилл, Удмуртская республика, г. Ижевск

### Вы можете меня найти:
- ВКонтакте: https://vk.com/id30907580
- Telegram: https://t.me/Kirill_Barabanshchikov
- Дзен: https://dzen.ru/bks_daily

## Технологии
- Python:3.9
- Django 3.2.3
- DjangoRestFramework 3.12.4

## Обратная связь
По всем вопросам работы проекта, а так же по вопросам размещения рекламы пишите мне, на bks2408@mail.ru
