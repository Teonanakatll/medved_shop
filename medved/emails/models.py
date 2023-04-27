from django.db import models

class EmailType(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип имейла'
        verbose_name_plural = 'Типы имейла'

# Модель для хранения всех отправленных имейлов
class EmailSendingFact(models.Model):
    type = models.ForeignKey(EmailType, on_delete=models.DO_NOTHING)
    # Если имейл связан с любым заказом
    order = models.ForeignKey("orders.Order", on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    email = models.EmailField()  # Кому отправлялся имейл
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = 'Отпрваленный имейл'
        verbose_name_plural = 'Отправленные имейлы'