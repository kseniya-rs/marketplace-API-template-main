from django.urls import path
from .apps import CustomUserConfig
from .views import CustomersListView, CustomerCreateView


app_name = CustomUserConfig.name


urlpatterns = [
    path('', CustomersListView.as_view(), name='custom_user_list'),
    path('create/', CustomerCreateView.as_view(), name='custom_user_create')
    ]
