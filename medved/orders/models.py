from django.db import models

from products.models import Product


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_activ = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'Статус {self.name}'

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

class Order(models.Model):
    # null=True устанавливает значение поля в NULL т.е. нет данных, относится к значению столбца БД
    # blank=True определяет будет ли поле обязательным в формах
    # blank=True null=True означает поле является необязательным при любых обстоятельствах
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for oll products in order
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    # Добавляет дату создания модели
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    # Добавляет дату изменения модели
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"Заказ {self.id, self.status.name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price * nmb
    is_activ = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

