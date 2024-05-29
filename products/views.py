from rest_framework import generics, status
from rest_framework.response import Response
from products.models import Product
from products.permissions import IsSeller, IsSuperUser, IsShopOwner
from products.serializers import ProductSerializer, ProductSaleStatusSerializers


class ProductCreateView(generics.CreateAPIView):
    """
    Контроллер для публикации продукта.
    Доступ к контроллеру имеется только у суперпользователя и пользователей со статусом "Продавец".
    """

    serializer_class = ProductSerializer
    permission_classes = [IsSeller | IsSuperUser]

    def perform_create(self, serializer):

        new_product = serializer.save(seller=self.request.user)
        new_product.seller = self.request.user

        total_price = new_product.calculate_final_price()
        new_product.price = total_price
        new_product.save()


class ProductListView(generics.ListAPIView):
    """
    Контроллер для просмотра размещенных на площадке товарах.
    Суперпользователь видит все размещенные на маркетплейсы товары, даже те, которые сняты с продажи.
    Продавец видит список всех своих товаров.
    Обычный пользователь может видеть все товары, которые находятся в активной продаже.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()

        if self.request.user.is_seller:
            return Product.objects.filter(seller=self.request.user)

        return Product.objects.filter(is_active_sale=True)


class ChangeProductSaleStatus(generics.UpdateAPIView):
    """
    Контроллер, отвечающий за снятие товара с продажи.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSaleStatusSerializers
    permission_classes = [IsShopOwner | IsSuperUser]

    def get_object(self):
        product = super().get_object()

        if product.is_active_sale:
            product.is_active_sale = False

        else:
            product.is_active_sale = True

        product.save()
        return product

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if instance.is_active_sale:
            sale_status_message = 'выведен в продажу'
        else:
            sale_status_message = 'снят с продажи'

        response_message = {
            "Product info": {'sale status': f'{instance.is_active_sale}',
                             'message': f'{instance.product_title} {sale_status_message}',
                             'status': status.HTTP_200_OK
                             }
        }

        return Response(response_message)


class ProductUpdateView(generics.UpdateAPIView):
    """
    Контроллер для редактирования информации о товаре.
    В отличие от ChangeProductSaleStatus, данный контроллер позволяет менять не только статус продажи,
    но и любую иную информацию. Доступ к контроллеру имеет владелец магазина или суперпользователь.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsShopOwner | IsSuperUser]


class ProductDetailView(generics.RetrieveAPIView):
    """
    Контроллер для просмотра детальной информации о товаре.
    Суперпользователь может просматривать все размещенные на маркетплейсы товары, даже те, которые сняты с продажи.
    Продавец может просматривать информацию только о своих товарах.
    Обычный пользователь может просматривать информацию только о тех товарах, которые находятся в активной продаже.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()

        if self.request.user.is_seller:
            return Product.objects.filter(seller=self.request.user)

        return Product.objects.filter(is_active_sale=True)


class ProductDeleteView(generics.DestroyAPIView):
    """
    Контроллер для удаления размещенного на площадке товара.
    Удалить товар может только тот продавец, который разместил данный товар.
    Суперпользователь может удалить любой размещенный товар.
    """

    queryset = Product.objects.all()
    permission_classes = [IsShopOwner | IsSuperUser]
