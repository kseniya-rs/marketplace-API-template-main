from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from custom_user.models import CustomUser


class ProductCreateTestCase(APITestCase):

    def setUp(self) -> None:
        """Предварительное наполнение БД для дальнейших тестов."""

        self.seller = CustomUser.objects.create(
            is_seller=True,
            shop_name="ASOS",
            email="asos@shop.com",
            password="123654"
        )

        self.common_user = CustomUser.objects.create(
            first_name="Alex",
            last_name="Abramov",
            email="common@user.ru",
            phone="800000000",
            password="123654",
        )

        self.product_data = {
            'product_title': 'Product Title',
            'price': '1000'
        }

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()

    def test_success_product_create(self):
        """Успешное создание нового товара продавцом"""

        self.client.force_authenticate(user=self.seller)
        response = self.client.post(reverse('products:create-product'), data=self.product_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {
                             'id': 3,
                             'shop_title': 'ASOS',
                             'seller': 'asos@shop.com',
                             'product_title': 'Product Title',
                             'price': '1300.00',
                             'is_active_sale': True
                         }
                         )

    def test_restrict_permission(self):
        """Тестирование ограничения доступа к размещению товара обычным пользователем"""

        self.client.force_authenticate(user=self.common_user)
        response = self.client.post(reverse('products:create-product'), data=self.product_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
