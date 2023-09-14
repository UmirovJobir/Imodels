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
    ConfiguratorProductInline,
    CartItemInline,
    OrderItemInline
)
from .models import (
    Category,
    Product,
    Blog,
    ContactRequest,
    Type,
    Item,
    Cart,
    Order,
)

admin.site.register(Type)
admin.site.register(Item)

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

    list_display = ['id', 'title', 'category_name', 'price', 'image_tag', 'status'] #description_short
    list_display_links = ['id', 'title']
    raw_id_fields = ['category']
    list_filter = [ProductFilter]
    inlines = [
        ProductImageInline,
        ProductVideoInline,
        ExtraDescriptionInline,
        ProductFeatureInline,
        ConfiguratorProductInline
    ]
    fieldsets = [
        ("Продукт", {
            "fields": ["related_configurator", "title", "description", "category", "price", "status"],
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



@admin.register(Order)
class OrderAdmin(NestedModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    readonly_fields = ['total_price']
    inlines = [OrderItemInline]