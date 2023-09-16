from rest_framework import permissions


class RecipePermissions(permissions.BasePermission):
    '''Права доступа к рецептам.'''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        if request.method == 'PATCH' or request.method == 'DELETE':
            if request.user == obj.author:
                return True
