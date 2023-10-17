from django import forms
from django.db import models
from django.forms import widgets
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.html import format_html

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
    DescriptionPoint,
)
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Type)

@admin.register(Description)
class DescriptionAdmin(TranslationAdmin, NestedModelAdmin):
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

    list_display = ['id', 'title', 'description_short', 'popular']
    list_display_links = ['id', 'title']
    summernote_fields = ['text']
    fieldsets = [
        (None, {
            "fields": [
                "popular",
                "title",
                "description",
                "text"
            ]
        }
        )
    ]

    def description_short(self, obj: Blog) -> str:
        if obj.description:
            if len(obj.description) < 48:
                return obj.description
            else:
                return obj.description[:48] + "..."
        else:
            return obj.description


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
class ProductAdmin(TranslationAdmin, NestedModelAdmin, SummernoteModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
        models.BooleanField: {
            'widget': widgets.NullBooleanSelect(attrs={
                'style': 'padding: 4px 8px; border-radius: 5px;'
            })
        },
    }

    summernote_fields = ['information']

    list_per_page = 20
    list_display = ['id', 'title', 'order_by', 'category_name', 'price', 'image_tag', 'status']
    list_display_links = ['id', 'title']
    raw_id_fields = ['category', 'configurator']
    list_filter = [ProductFilter]
    inlines = [
        # ExtraDescriptionInline,
        ProductImageInline,
        ProductVideoInline,
        ProductFeatureInline,
        ItemInline,
    ]
    fieldsets = [
        ("Продукт", {
            "fields": [
                "is_configurator",
                "configurator",
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
    
    def image_tag(self, obj):
        try:
            first_image = obj.product_images.first().image.url
        except AttributeError:
            first_image = "/static/img/no-image.png"
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(first_image))
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('product_images', 'items', 'item', 'item__type') \
            .select_related('category', 'configurator', 'product_video', 'product_features', 'product_description')
        return queryset


@admin.register(Order)
class OrderAdmin(NestedModelAdmin):
    list_display = ['id', 'customer', 'total_price', 'order_status']
    list_display_links = ['id', 'customer']
    readonly_fields = ['formatted_total_price', 'order_status', 'created_at']
    inlines = [OrderProductInline]
    fieldsets = [
        ("Order", {
            "fields": [
                "customer",
                "order_status",
                "formatted_total_price",
                "created_at"
            ],
        }),
    ]
    
    def formatted_total_price(self, obj):
        return "{:,.2f} So'm".format(obj.total_price)
    formatted_total_price.short_description = 'Total Price'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('customer')
        return queryset
    
    def order_status(self, obj):
        #ff0000; /* Red */
        # css = "color: white; padding: 4px 8px; border-radius: 5px; background-color: {}"
        return format_html(
            """<span 
                style="
                color: black;
                padding: 4px 8px;
                border-radius: 5px;
                background-color: {}
                ">{}
            </span>""",
                '#09E502' if obj.status=="To'langan" else '#FFF404',
                obj.status)

    

