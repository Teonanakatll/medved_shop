from django.contrib import admin
from .models import Product, ProductImage, ProductCategory

# For import-export
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

admin.site.register(ProductCategory, ProductCategoryAdmin)

# Cоздать запись в БД, на которую ссылается ForeignKey во всплывающем окне
class ProductImageInline(admin.TabularInline):
    # Связанная модель
    model = ProductImage
    # Количество дополнительных ссылок для добавления связанных вторичных моделей
    extra = 0

class ProductResource(resources.ModelResource):
    # Для отображения вместо id ForeignKey, название первичного класса
    # faculty = fields.Field(column_name='faculty', attribute='faculty', widget=ForeignKeyWidget(Faculty, 'name'))
    # module = fields.Field(column_name='module', attribute='module', widget=ForeignKeyWidget(Module, 'name'))
    # type = fields.Field(column_name='type', attribute='type', widget=ForeignKeyWidget(ClassType, 'name'))
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(ProductCategory, 'name'))

    class Meta:
        model = Product

class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = [field.name for field in Product._meta.fields if field.name != "id"]
    # Отображение и добавление связанных вторичных моделей (фотографий)
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'price', 'discount', 'category')
#     # exclude = ('description',)
#     list_display_links = ('id', 'name')
#     # Отображение и добавление связанных вторичных моделей
#     inlines = (ProductImageInline,)
#     list_filter = ('is_activ', 'created')
#     list_editable = ('category', 'discount')
#
# admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]
    list_filter = ('is_activ', 'created')
    list_editable = ('is_main',)

admin.site.register(ProductImage, ProductImageAdmin)
