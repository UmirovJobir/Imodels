from django import forms
from django.db import models
from django.contrib import admin

from tinymce.widgets import TinyMCE
from nested_admin import NestedModelAdmin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .admin_filters import CategoryFilter, ProductFilter
from .admin_inlines import (
    CategoryInline,
    ProductImageInline,
    ProductVideoInline,
    ExtraDescriptionInline,
    ProductFeatureInline,
    ConfiguratorInline,
    ConfiguratorCategoryInline,
    CartItemInline,
)
from .models import (
    Category,
    Product,
    Blog,
    ContactRequest,
    Configurator,
    Cart,
)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price']
    list_display_links = ['id', 'total_price']
    inlines = [CartItemInline]
    readonly_fields = ['total_price']


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone_number', 'message_short']
    list_display_links = ['id', 'name']

    def message_short(self, obj: ContactRequest) -> str:
        if len(obj.message) < 48:
            return obj.message
        else:
            return obj.message[:48] + "..."


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'description_short']
    list_display_links = ['id', 'title']

    def description_short(self, obj: Blog) -> str:
        if len(obj.text) < 48:
            return obj.text
        else:
            return obj.text[:48] + "..."
    
    class Media:
        js = ('js/uploader.js',)


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
class ProductAdmin(TranslationAdmin, NestedModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 130, 'rows': 20})},
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }

    list_display = ['id', 'title', 'category_name', 'price', 'image_tag'] #description_short
    list_display_links = ['id', 'title']
    raw_id_fields = ['category']
    list_filter = [ProductFilter]
    inlines = [
        ProductImageInline,
        ProductVideoInline,
        ExtraDescriptionInline,
        ProductFeatureInline,
        ConfiguratorInline
    ]
    fieldsets = [
        ("Продукт", {
            "fields": ["related_configurator", "title", "description", "category", "price"],
            "classes": ["wide"],
        }),
    ]
    
    def category_name(self, obj: Product) -> str:
        return obj.category.name

    def description_short(self, obj: Product) -> str:
        print(obj.description)
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."


@admin.register(Configurator)
class ConfiguratorAdmin(NestedModelAdmin):
    list_display = ['id', 'conf_title', 'conf_image', 'image_tag']
    list_display_links = ['id', 'conf_title']
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'product_image_tag']
    inlines = [ConfiguratorCategoryInline]

    fieldsets = [
        ("Configurator", {
            "fields": ['conf_title', 'conf_image', 'image_tag', 'product', 'product_image_tag'],
        }),
    ]

