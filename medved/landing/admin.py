from django.contrib import admin
from .models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    # list_display =("name", "email")

    # Вывод полей стандартным питоновским итератором из модели Subscribers
    list_display = [field.name for field in Subscriber._meta.fields]

    # Поля по которым можно фильтровать записи (сайд-бар)
    list_filter = ("name",)

    # Поля по каким можно производить поиск
    search_fields = ("name",)

    # Будут отображаться все поля кроме исключенных
    # exclude = ()


    class Meta:
        model = Subscriber

admin.site.register(Subscriber, SubscriberAdmin)
