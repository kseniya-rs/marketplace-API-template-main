from django.contrib.auth import get_user_model
from django.db import models
from decimal import Decimal


class Product(models.Model):
    """
    Модель для хранения информации о товаре.
    """

    SALE_STATUS = [
        (True, 'В продаже'),
        (False, 'Снят с продажи')
    ]

    product_title = models.CharField(max_length=255, verbose_name='Наименование товара')
    seller = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                               related_name='seller', verbose_name='Продавец')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    is_active_sale = models.BooleanField(default=True, choices=SALE_STATUS, verbose_name='Статус товара')

    objects = models.Manager

    @property
    def shop_name(self):
        return self.seller.shop_name

    def calculate_final_price(self):
        """
        Расчет финальной стоимости товара
        """

        base_price = self.price
        tax = base_price * Decimal('0.06')  #: Налог
        bank_fee = base_price * Decimal('0.02')  #: Комиссия банку
        author_commission = base_price * Decimal('0.02')  #: Комиссия за транзакцию продавца
        marketplace_fee = base_price * Decimal('0.20')  #: Выручка маркетплейса

        final_price = base_price + tax + bank_fee + author_commission + marketplace_fee
        return final_price

    def __str__(self):
        return f'{self.product_title} {self.shop_name} {self.seller}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
