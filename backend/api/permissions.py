from rest_framework import permissions


class ReadOrAddUpdateDelRecipePermissions(permissions.BasePermission):
    """Права доступа к рецептам."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.method == 'POST' and request.user.is_authenticated)
            or (
                (request.method == 'PATCH' or request.method == 'DELETE')
                and request.user == obj.author
            )
        )
