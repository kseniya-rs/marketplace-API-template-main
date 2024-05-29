from django.urls import path
from .apps import ProductsConfig
from . import views


app_name = ProductsConfig.name


urlpatterns = [
    path('create/', views.ProductCreateView.as_view(), name='create-product'),
    path('list/', views.ProductListView.as_view(), name='products-list'),
    path('change_status/<int:pk>/', views.ChangeProductSaleStatus.as_view(), name='change-sale-status'),
    path('edit_product/<int:pk>/', views.ProductUpdateView.as_view(), name='edit-product'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),
    ]
