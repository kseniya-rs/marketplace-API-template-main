from django.contrib import admin
from products.models import Product


@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'product_title', 'seller', 'price', 'is_active_sale', )
    list_display_links = ('product_title', )
