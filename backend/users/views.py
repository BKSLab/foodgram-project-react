from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Subscription
from users.models import User
from users.serializers import SubscriptionsSerializer


class UserRegistrationViewSet(UserViewSet):
    """viewset для регистрации пользователей на сайте."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=['get'],
        serializer_class=SubscriptionsSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request, *args, **kwargs):
        """Выдача подписок пользователя."""
        authors = self.paginate_queryset(
            Subscription.objects.filter(
                user=request.user,
            )
        )
        serializer = SubscriptionsSerializer(
            authors,
            many=True,
            context={
                'request': request,
            },
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        url_path=r'(?P<id>\d+)/subscribe',
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, *args, **kwargs):
        """Подписка и отписка от авторов."""
        user = request.user
        author = get_object_or_404(User, id=kwargs.get('id'))
        check_subscription = Subscription.objects.filter(
            user=user,
            author=author,
        ).exists()
        if request.method == 'POST':
            if author.id == user.id:
                return Response(
                    {'errors': 'так не пойдет, подписаться на себя нельзя!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if check_subscription:
                return Response(
                    {'errors': 'так не пойдет, ты уже подписался на автора'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            author_sub = Subscription.objects.create(
                user=user,
                author=author,
            )
            serializer = SubscriptionsSerializer(
                author_sub,
                context={
                    'request': request,
                },
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if check_subscription:
                Subscription.objects.filter(
                    user=user,
                    author=author,
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'так не пойдет, ты не подписывался на автора'},
                status=status.HTTP_400_BAD_REQUEST,
            )
