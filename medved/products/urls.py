from django.urls import path
from products.views import product

urlpatterns = [
    path('product/<int:product_id>/', product, name='product')
]