from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    ExtraDescription,
    Description,
)

class DescriptionInline(admin.StackedInline):
    model = Description
    extra = 0

@admin.register(ExtraDescription)
class AdditionalDescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_short', 'product_name']
    list_display_links = ['id', 'title_short']
    raw_id_fields = ['product']
    inlines = [DescriptionInline]

    def product_name(self, obj: ExtraDescription) -> str:
        return f"ID: {obj.product.id}, Title: {obj.product.title}"

    def title_short(self, obj: ExtraDescription) -> str:
        if len(obj.title) < 48:
            return obj.title
        else:
            return obj.title[:48] + "..."

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']
    raw_id_fields = ['parent']


class ProductVideoInline(admin.StackedInline):
    model = ProductVideo
    extra = 0

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'price', 'category_name', 'description_short']
    list_display_links = ['id', 'title']
    raw_id_fields = ['category']
    inlines = [ProductImageInline, ProductVideoInline]

    
    def category_name(self, obj: Product) -> str:
        return obj.category.name

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."


