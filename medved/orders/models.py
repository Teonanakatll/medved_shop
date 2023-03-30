from django.db import models
from django.db.models.signals import post_save

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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for oll products in order
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

    # def save(self, *args, **kwargs):
    #     super(ProductInOrder, self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        # Переменные сохранятся в модель только после отрабатывания всей фгнкции полностью,
        # поэтому в дальнейших расчетах с данными бд до сохранения модели, не будет учитываться
        # для корректных расчётов необходимо воспользоваться функцией post-save()
        self.total_price = self.nmb * self.price_per_item

        # Присваиваем переменной order ссылку на связанный первичный класс модели
        # order = self.order
        # all_products_in_order = ProductInOrder.objects.filter(order=order, is_activ=True)
        #
        # order_total_price = 0
        # for item in all_products_in_order:
        #     order_total_price += item.total_price
        #
        # # Присваиваем полю total_price связанной первичной модели результат слажения
        # self.order.total_price = order_total_price
        # # При сохранении обновить текущую запись
        # self.order.save(force_update=True)

        super(ProductInOrder, self).save(*args, **kwargs)

# Cохраняет что-либо только не для sender-модели иначе будет вызываться снова и снова
# Ecли нужно сохранить что-либо для той же модели, нужно переопределять метод save()
def product_in_order_post_save(sender, instance, created, **kwargs):
    # Присваиваем переменной order ссылку на связанный первичный класс модели
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_activ=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

        # Присваиваем полю total_price связанной первичной модели результат слажения
        instance.order.total_price = order_total_price
        # При сохранении обновить текущую запись
        instance.order.save(force_update=True)

# post_save слушает сигнал класса ProductInOrder присоединяет функцию product_in_order_post_save
# и сохраняет изменения в св. пр. класс order
post_save.connect(product_in_order_post_save, sender=ProductInOrder)