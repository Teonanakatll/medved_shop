from django.contrib import admin
from .models import Product, ProductImage, ProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

admin.site.register(ProductCategory, ProductCategoryAdmin)

# Cоздать запись в БД, на которую ссылается ForeignKey во всплывающем окне
class ProductImageInline(admin.TabularInline):
    # Связанная модель
    model = ProductImage
    # Количество дополнительных ссылок для добавления связанных вторичных моделей
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount', 'category')
    # exclude = ('description',)
    list_display_links = ('id', 'name')
    # Отображение и добавление связанных вторичных моделей
    inlines = (ProductImageInline,)
    list_filter = ('is_activ', 'created')
    list_editable = ('category', 'discount')

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]
    list_filter = ('is_activ', 'created')
    list_editable = ('is_main',)

admin.site.register(ProductImage, ProductImageAdmin)
