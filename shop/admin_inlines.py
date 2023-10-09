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


class ProductVideoInline(TranslationStackedInline, NestedStackedInline, SummernoteInlineModelAdmin): #admin.StackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductVideo
    classes = ['collapse']
    # readonly_fields = ['video_tag']


class ProductImageInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = ProductImage
    classes = ['collapse']
    readonly_fields = ['image_tag']


class ProductFeaturePointInline(TranslationStackedInline, NestedStackedInline): #, admin.StackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductFeaturePoint


class ProductFeatureInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeaturePointInline]
    classes = ['collapse']
    readonly_fields = ['image_tag']


class DescriptionPointInline(TranslationTabularInline, NestedTabularInline, SummernoteInlineModelAdmin):
    extra = 0
    model = DescriptionPoint


class DescriptionImageInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = DescriptionImage
    readonly_fields = ['image_tag']


class DescriptionInline(TranslationStackedInline, NestedStackedInline): #, admin.StackedInline):
    # formfield_overrides = {
    #     # models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    # }
    extra = 0
    model = Description
    inlines = [DescriptionImageInline, DescriptionPointInline]
    classes = ['collapse']


class ItemInline(NestedTabularInline): #admin.TabularInline):
    extra = 0
    model = Item
    fk_name = 'item'
    raw_id_fields = ['type', 'product']
    readonly_fields = ['price', 'image_tag']
    classes = ['collapse']


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
