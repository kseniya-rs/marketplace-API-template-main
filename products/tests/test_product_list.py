from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from custom_user.models import CustomUser
from products.models import Product


class ProductListTestCase(APITestCase):

    def setUp(self) -> None:
        """Предварительное наполнение БД для дальнейших тестов."""

        self.seller = CustomUser.objects.create(
            is_seller=True,
            shop_name='ASOS',
            email='asos@shop.com',
            password='123654'
        )

        self.product = Product.objects.create(
            seller=self.seller,
            product_title='Product Title',
            price='1000.00'
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.seller)

    def test_product_list(self):
        """Тест для проверки вывода списка продуктов"""

        response = self.client.get(reverse('products:products-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()[0],
                         {
                             'id': self.product.id,
                             'shop_title': self.seller.shop_name,
                             'seller': self.seller.email,
                             'product_title': self.product.product_title,
                             'price': '1000.00',
                             'is_active_sale': True
                         }
                         )
