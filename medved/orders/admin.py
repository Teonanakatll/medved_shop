from django.contrib import admin
from .models import Status, Order, ProductInOrder

# Класс для вставки в админку модели связанных с ней вторичных моделей
class ProductInOrderInline(admin.TabularInline):
    # Связанная модель
    model = ProductInOrder
    # Количество дополнительных ссылок для загрузки картинок под постом
    extra = 0

class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]
    list_filter = ('is_activ', 'created')

admin.site.register(Status, StatusAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    list_display_links = ('customer_name',)
    # Отображение связанных моделей
    inlines = (ProductInOrderInline,)
    list_filter = ('status', 'created')

admin.site.register(Order, OrderAdmin)

class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]
    list_filter = ('is_activ', 'created')

admin.site.register(ProductInOrder, ProductInOrderAdmin)