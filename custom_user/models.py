from django.contrib.auth.models import AbstractUser
from django.db import models
from custom_user.services import shop_preview_upload_path
from custom_user.user_manager import CustomUserManager


NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    """
    Расширение стандартной модели пользователя в соответствии с требованиями текущего проекта.
    """

    class UserStatus(models.IntegerChoices):
        """
        Вспомогательный класс для определения статуса посетителя магазина.
        По умолчанию, каждый новый пользователь имеет статус 'Посетитель'.
        """

        COMMON_USER = 0, "Посетитель"
        SELLER = 1, "Продавец"

    username = None

    # Поля, используемые для регистрации посетителя сайта
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)

    # Поля, используемые для регистрации продавца
    shop_name = models.CharField(max_length=200, verbose_name='Название магазина', **NULLABLE)
    shop_preview = models.ImageField(upload_to=shop_preview_upload_path, verbose_name='Превью магазина', **NULLABLE)

    # Общие поля для каждого вида пользователя
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Статус активации')
    is_seller = models.BooleanField(choices=UserStatus.choices, default=UserStatus.COMMON_USER,
                                    verbose_name='Статус клиента')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
