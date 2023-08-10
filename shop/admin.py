from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'parent', 'name'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'price', 'category_name', 'description_short'
    list_display_links = 'id', 'title'
    
    def category_name(self, obj: Product) -> str:
        return obj.category.name['uz_latn']

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = 'id', 'image', 'product'
    list_display_links = 'id', 'image',

