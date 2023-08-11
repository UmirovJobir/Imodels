from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    Category,
    Product,
    ProductImage,
)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'price', 'category_name', 'description_short']
    list_display_links = ['id', 'title']
    inlines = [ProductImageInline]

    
    def category_name(self, obj: Product) -> str:
        return obj.category.name

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."


