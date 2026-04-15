from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Кастомна перевірка: дозволяє доступ ТІЛЬКИ адміністраторам (superuser або staff).
    """
    def has_permission(self, request, view):
        # Повертає True, якщо користувач авторизований і є адміном
        return bool(request.user and request.user.is_staff)