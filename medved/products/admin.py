from django.contrib import admin
from .models import Product, ProductImage

# Класс для вставки в админку модели связанных с ней вторичных моделей
class ProductImageInline(admin.TabularInline):
    # Связанная модель
    model = ProductImage
    # Количество дополнительных ссылок для загрузки картинок под постом
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_display_links = ('id', 'name')
    # Присваиваем переменной ссылку на класс со связанными картинками
    inlines = (ProductImageInline,)
    list_filter = ('is_activ', 'created')

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]
    list_filter = ('is_activ', 'created')

admin.site.register(ProductImage, ProductImageAdmin)
