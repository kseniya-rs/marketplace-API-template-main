from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class CommonUserCreateTestCase(APITestCase):

    def test_success_creation(self):
        """Тесткейс успешного создания нового продавца"""

        seller_data: dict = {
            "is_seller": True,
            "shop_name": "ASOS",
            "email": "asos@shop.com",
            "password": "123654",
            "password_confirmation": "123654"
        }

        response = self.client.post(reverse('custom_user:custom_user_create'), data=seller_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'message': 'Вы зарегистрированы в качестве продавца и можете размещать товары на площадке',
                          'shop_title': 'ASOS',
                          'status': 201})

    def test_failed_password_confirmation(self):
        """Тесткейс при неверной передачи значения password_confirmation"""

        seller_data: dict = {
            "is_seller": True,
            "shop_name": "ASOS",
            "email": "asos@shop.com",
            "password": "123654",
            "password_confirmation": "000000"
        }

        response = self.client.post(reverse('custom_user:custom_user_create'), data=seller_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Пароль и его подтверждение не совпадают']})

    def test_no_password_confirmation(self):
        """Тесткейс при отсутствии значения password_confirmation"""

        seller_data: dict = {
            "is_seller": True,
            "shop_name": "ASOS",
            "email": "asos@shop.com",
            "password": "123654",
        }

        response = self.client.post(reverse('custom_user:custom_user_create'), data=seller_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'password_confirmation': ['Обязательное поле.']})
