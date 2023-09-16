from django.urls import include, path

from rest_framework import routers

from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from users.views import UserRegistrationViewSet

router = routers.DefaultRouter()

router.register('users', UserRegistrationViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
