from django import forms
from django.db import models
from django.contrib import admin

from nested_admin import NestedModelAdmin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .admin_filters import CategoryFilter, ProductFilter
from .admin_inlines import (
    CategoryInline,
    ProductImageInline,
    ProductVideoInline,
    DescriptionInline,
    DescriptionImageInline,
    DescriptionPointInline,
    ProductFeatureInline,
    ItemInline,
    OrderProductInline,
)
from .models import (
    Category,
    Product,
    Blog,
    ContactRequest,
    Type,
    Item,
    Order,
    ProductVideo,
    ProductImage,
    Description,
    DescriptionPoint
)
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Type)

@admin.register(Description)
class DescriptionAdmin(TranslationAdmin, NestedModelAdmin  ):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 170})},
    }
    inlines = [DescriptionImageInline, DescriptionPointInline]


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'message_short']
    list_display_links = ['id', 'name']

    def message_short(self, obj: ContactRequest) -> str:
        if obj.message:
            if len(obj.message) < 48:
                return obj.message
            else:
                return obj.message[:48] + "..."
        return None

@admin.register(Blog)
class BlogAdmin(TranslationAdmin, SummernoteModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 170})},
    }

    list_display = ['id', 'title', 'description_short']
    list_display_links = ['id', 'title']
    summernote_fields = ['text']

    def description_short(self, obj: Blog) -> str:
        if obj.description:
            if len(obj.description) < 48:
                return obj.description
            else:
                return obj.description[:48] + "..."
        else:
            return obj.description
    
    # class Media:
    #     js = ('js/uploader.js',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name_uz', 'name_ru', 'name_en', 'parent']
    list_display_links = ['id', 'name_uz']
    raw_id_fields = ['parent']
    list_filter = [CategoryFilter]
    fieldsets = [
        ("КАТЕГОРИЯ", {
            "fields": ("parent", "name"),
            "classes":("collapse"),
            "description":"Родительская категория",
        }),
    ]


@admin.register(Product)
class ProductAdmin(TranslationAdmin, NestedModelAdmin, SummernoteModelAdmin): #, admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }

    summernote_fields = ['information']

    list_per_page = 20
    list_display = ['id', 'title', 'order_by', 'category_name', 'price', 'image_tag', 'status'] #description_short
    list_display_links = ['id', 'title']
    raw_id_fields = ['category', 'set_creator']
    list_filter = [ProductFilter]
    inlines = [
        ProductImageInline,
        ProductVideoInline,
        # ExtraDescriptionInline,
        ProductFeatureInline,
        ItemInline
    ]
    fieldsets = [
        ("Продукт", {
            "fields": [
                "set_creator",
                "title",
                "order_by",
                "information",
                "category",
                "price",
                "status"
            ],
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
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_price']
    list_display_links = ['id', 'customer']
    readonly_fields = ['total_price']
    inlines = [OrderProductInline]