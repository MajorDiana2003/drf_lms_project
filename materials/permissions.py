from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, входит ли пользователь в группу модераторов."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Проверяем, существует ли у пользователя группа с именем 'модераторы'
            return request.user.groups.filter(name="модераторы").exists()
        return False


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):
        # Доступ разрешен, только если владелец объекта — это текущий пользователь
        return obj.owner == request.user
