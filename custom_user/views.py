from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from custom_user.models import CustomUser
from custom_user import serializers


class CustomersListView(generics.ListAPIView):
    """Контроллер для отображения списка зарегистрированных пользователей."""

    serializer_class = serializers.CustomersListSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('is_seller', )
    permission_classes = [IsAdminUser]


class CustomerCreateView(generics.CreateAPIView):
    """Контроллер для регистрации новых пользователей."""

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """
        Метод переопределен для выбора конкретного сериализатора в зависимости от переданных в POST запросе данных.
        """

        is_seller = self.request.data.get('is_seller', None)

        if is_seller:
            return serializers.SellerSerializer

        return serializers.VisitorSerializer

    def create(self, request, *args, **kwargs):
        is_seller = request.data.get('is_seller', False)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if is_seller:
                # Если выбран статус продавца, устанавливаем его
                serializer.save(is_seller=CustomUser.UserStatus.SELLER)
                return Response(
                    {'message': 'Вы зарегистрированы в качестве продавца и можете размещать товары на площадке',
                     'shop_title': f'{serializer.data.get("shop_name")}',
                     'status': status.HTTP_201_CREATED})

            else:
                # Если выбран статус посетителя, оставляем его по умолчанию
                serializer.save()
                return Response({'message': 'Регистрация успешно завершена!',
                                 'status': status.HTTP_201_CREATED})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
