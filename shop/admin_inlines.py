from django import forms
from django.db import models
from django.forms import widgets
from django.contrib import admin
from django.utils.html import mark_safe
from nested_admin import NestedStackedInline, NestedTabularInline
from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.admin import SummernoteInlineModelAdmin

from .models import (
    Category,
    ProductImage,
    ProductVideo,
    Description,
    DescriptionPoint,
    ProductFeature,
    ProductFeaturePoint,
    ProductGallery,
    Type,
    Item,
    Order,
    OrderProduct,
)

class CategoryInline(TranslationTabularInline):
    extra = 0
    model = Category
    verbose_name = "Подкатегория"
    verbose_name_plural = "Подкатегории"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('parent')
        return queryset


class ProductVideoInline(NestedStackedInline, TranslationStackedInline, SummernoteInlineModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductVideo
    classes = ['collapse']
    # readonly_fields = ['video_tag']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class ProductImageInline(NestedTabularInline):
    extra = 0
    model = ProductImage
    classes = ['collapse']
    readonly_fields = ['image_tag']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class ProductFeaturePointInline(NestedStackedInline, TranslationStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductFeaturePoint

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class ProductFeatureInline(NestedTabularInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeaturePointInline]
    classes = ['collapse']
    readonly_fields = ['image_tag']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('features')
        return queryset


class ProductGalleryInline(NestedTabularInline):
    extra = 0
    model = ProductGallery
    readonly_fields = ['image_tag']
    classes = ['collapse']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class DescriptionPointInline(TranslationTabularInline, NestedTabularInline, SummernoteInlineModelAdmin):
    extra = 0
    model = DescriptionPoint

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('description')
        return queryset


class DescriptionInline(NestedStackedInline, TranslationStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 200})},
    }
    extra = 0
    model = Description
    inlines = [DescriptionPointInline]
    classes = ['collapse']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('description_points')
        return queryset


class ItemInline(NestedTabularInline):
    extra = 0
    model = Item
    fk_name = 'item'
    raw_id_fields = ['type', 'product']
    readonly_fields = ['price', 'image_tag']
    classes = ['collapse']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('type', 'product', 'item')
        return queryset


class OrderProductInline(NestedTabularInline):
    formfield_overrides = {
        models.PositiveIntegerField: {
            'widget': widgets.NumberInput(attrs={
                'style':  'width: 50px;'  #'padding: 4px 8px; border-radius: 5px;'
            })
        },
        models.DecimalField: {
            'widget': widgets.NumberInput(attrs={
                'style':  'width: 100px;'  #'padding: 4px 8px; border-radius: 5px;'
            })
        }
    }
    extra = 0
    model = OrderProduct
    raw_id_fields = ['product', 'configurator']
    readonly_fields = ['product', 'configurator', 'image_tag', 'formatted_subtotal_price', 'product_name']
    fieldsets = [
        (None, {
            "fields": [
                'configurator',
                'product',
                'price',
                'price_usd',
                'price_eur',
                'quantity',
                'image_tag',
                'formatted_subtotal_price',
            ],
        }),
    ]

    def formatted_subtotal_price(self, obj):
        return "{:,.2f}".format(obj.subtotal)
    formatted_subtotal_price.short_description = 'Subtotal'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('order', 'product').prefetch_related('product__product_images', 'configurator').order_by('configurator')
        return queryset


 