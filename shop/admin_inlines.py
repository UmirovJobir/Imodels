from django import forms
from django.db import models
from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from nested_admin import NestedStackedInline, NestedTabularInline
from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.admin import SummernoteInlineModelAdmin

from .models import (
    Category,
    ProductImage,
    ProductVideo,
    Description,
    DescriptionImage,
    DescriptionPoint,
    ProductFeature,
    ProductFeaturePoint,
    Type,
    Item,
    Order,
    OrderProduct,
    OrderProductItem,
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


class ProductVideoInline(TranslationStackedInline, NestedStackedInline, SummernoteInlineModelAdmin): #admin.StackedInline):
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


class ProductImageInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = ProductImage
    classes = ['collapse']
    readonly_fields = ['image_tag']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class ProductFeaturePointInline(TranslationStackedInline, NestedStackedInline): #, admin.StackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductFeaturePoint

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class ProductFeatureInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeaturePointInline]
    classes = ['collapse']
    readonly_fields = ['image_tag']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('features')
        return queryset


class DescriptionPointInline(TranslationTabularInline, NestedTabularInline, SummernoteInlineModelAdmin):
    extra = 0
    model = DescriptionPoint

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('description')
        return queryset



class DescriptionImageInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = DescriptionImage
    readonly_fields = ['image_tag']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('description')
        return queryset


class DescriptionInline(TranslationStackedInline, NestedStackedInline): #, admin.StackedInline):
    # formfield_overrides = {
    #     # models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    # }
    extra = 0
    model = Description
    inlines = [DescriptionImageInline, DescriptionPointInline]
    classes = ['collapse']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('description_points', 'description_images')
        return queryset


class ItemInline(NestedTabularInline): #admin.TabularInline):
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


class OrderItemInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = OrderProductItem
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'subtotal']


class OrderProductInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = OrderProduct
    inlines = [OrderItemInline]
    # classes = ['collapse']
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'subtotal', 'total_price']
