from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Product.
    :shop_title Название магазина, указанное продавцом при регистрации. Значение берется из модели CustomUser.
    :seller Удобочитаемое отображение пользователя (email) вместо id пользователя.
    """

    shop_title = serializers.CharField(source='seller.shop_name', read_only=True)
    seller = serializers.CharField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSaleStatusSerializers(serializers.ModelSerializer):
    """
    Сериализатор используется в контроллере ChangeProductSaleStatus.
    """
    class Meta:
        model = Product
        fields = ('is_active_sale', )
