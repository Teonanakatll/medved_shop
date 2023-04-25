from django.urls import path
from .views import basket_adding, checkout, admin_orders


urlpatterns = [
    path('basket_adding/', basket_adding, name='basket_adding'),
    path('checkout/', checkout, name='checkout'),
    path('admin_orders/', admin_orders, name='admin_orders'),
]