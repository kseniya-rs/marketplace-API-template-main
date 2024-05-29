from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class CommonUserCreate(APITestCase):

    def test_success_creation(self):
        """Тесткейс успешного создания нового пользователя"""

        users_data: dict = {
            "first_name": "Alex",
            "last_name": "Abramov",
            "email": "common@user.ru",
            "phone": "800000000",
            "password": "123654",
            "password_confirmation": "123654"
        }

        response = self.client.post(reverse('custom_user:custom_user_create'), data=users_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'message': 'Регистрация успешно завершена!',
                          'status': status.HTTP_201_CREATED})

    def test_failed_password_confirmation(self):
        """Тесткейс при неверной передачи значения password_confirmation"""

        users_data: dict = {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "common@user.ru",
            "phone": "800000000",
            "password": "123654",
            "password_confirmation": "000000"
        }

        response = self.client.post(reverse('custom_user:custom_user_create'), data=users_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Пароль и его подтверждение не совпадают']})

    def test_no_password_confirmation(self):
        """Тесткейс при отсутствии значения password_confirmation"""

        users_data: dict = {
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "common@user.ru",
            "phone": "800000000",
            "password": "123654"
        }

        response = self.client.post(reverse('custom_user:custom_user_create'), data=users_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'password_confirmation': ['Обязательное поле.']})
