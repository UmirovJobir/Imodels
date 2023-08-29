import nested_admin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .admin_filters import CategoryFilter
from .admin_inlines import (
    CategoryInline,
    ProductImageInline,
    ProductVideoInline,
    ExtraDescImageInline,
    ExtraDescriptionInline,
    ProductFeatureInline,
)
from .models import (
    Category,
    Product,
)



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']
    inlines = [CategoryInline]
    list_filter = [CategoryFilter]
    fieldsets = [
        ("КАТЕГОРИЯ", {
            "fields": ("name",),
            "classes":("collapse"),
            "description":"Родительская категория",
        }),
    ]


@admin.register(Product)
class ProductAdmin(TranslationAdmin, nested_admin.NestedModelAdmin):
    list_display = ['id', 'title', 'category_name', 'description_short', 'price']
    list_display_links = ['id', 'title']
    raw_id_fields = ['category']
    inlines = [ProductImageInline, ProductVideoInline, ExtraDescriptionInline, ProductFeatureInline]
    fieldsets = [
        ("Продукт", {
            "fields": ("title", "description", "category", "price"),
            "classes":("collapse"),
        }),
    ]

    
    def category_name(self, obj: Product) -> str:
        return obj.category.name

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."


