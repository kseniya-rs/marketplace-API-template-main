from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    """
    Данный класс предоставляет право доступа к контроллеру в том случае,
    если текущий пользователь имеет статус "Продавец".
    """

    def has_permission(self, request, view):
        return bool(request.user.is_seller)


class IsSuperUser(BasePermission):
    """
    Данный класс определяет права доступа для пользователей, у которых стоит флаг 'is_superuser'.
    В отличие от IsAdminUser, 'IsSuperUser' предоставляет доступ только суперпользователям.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsShopOwner(BasePermission):
    """
    Контроллер определяет доступ только к тем объектам, которые были созданы текущим авторизованным пользователем.
    """

    def has_object_permission(self, request, view, obj):

        if request.user == obj.seller:
            return True

        return False
