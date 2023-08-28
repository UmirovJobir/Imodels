from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
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

class ExtraDescriptionInline(admin.StackedInline):
    model = ExtraDescription
    extra = 0
    inlines = [DescriptionInline]

# @admin.register(ExtraDescription)
# class ExtraDescriptionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title_short', 'product_name']
#     list_display_links = ['id', 'title_short']
#     raw_id_fields = ['product']
#     inlines = [DescriptionInline]

#     def product_name(self, obj: ExtraDescription) -> str:
#         return f"ID: {obj.product.id}, Title: {obj.product.title}"

#     def title_short(self, obj: ExtraDescription) -> str:
#         if len(obj.title) < 48:
#             return obj.title
#         else:
#             return obj.title[:48] + "..."


class CategoryFilter(admin.SimpleListFilter):
    title = 'Родительские категории'
    parameter_name = 'subcategory'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in model_admin.model.objects.filter(parent__isnull=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__name=self.value())

class CategoryInline(TranslationTabularInline):
    extra = 0
    model = Category
    verbose_name = "Подкатегория"
    verbose_name_plural = "Подкатегории"

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


class ProductVideoInline(admin.StackedInline):
    model = ProductVideo
    extra = 0

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'category_name', 'description_short', 'price']
    list_display_links = ['id', 'title']
    raw_id_fields = ['category']
    inlines = [ProductImageInline, ProductVideoInline, ExtraDescriptionInline]

    
    def category_name(self, obj: Product) -> str:
        return obj.category.name

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."


