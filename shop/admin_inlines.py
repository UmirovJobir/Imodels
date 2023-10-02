from django import forms
from django.db import models
from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from nested_admin import NestedStackedInline, NestedTabularInline
from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline
from .models import (
    Category,
    ProductImage,
    ProductVideo,
    Description,
    ExtraDescImage,
    ExtraDescription,
    ProductFeature,
    ProductFeatureOption,
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


class ProductVideoInline(TranslationStackedInline, admin.StackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductVideo
    classes = ['collapse']
    # readonly_fields = ['video_tag']


class ProductImageInline(admin.TabularInline):
    extra = 1
    model = ProductImage
    classes = ['collapse']
    # readonly_fields = ['image_tag']


class ProductFeatureOptionsInline(TranslationStackedInline, admin.StackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductFeatureOption


class ProductFeatureInline(admin.TabularInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeatureOptionsInline]
    classes = ['collapse']
    readonly_fields = ['image_tag']


class DescriptionInline(TranslationTabularInline, admin.TabularInline):
    extra = 0
    model = Description


class ExtraDescImageInline(admin.TabularInline):
    extra = 0
    model = ExtraDescImage
    readonly_fields = ['image_tag']


class ExtraDescriptionInline(TranslationStackedInline, admin.StackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ExtraDescription
    inlines = [ExtraDescImageInline] #, DescriptionInline]
    classes = ['collapse']


class ItemInline(admin.TabularInline):
    extra = 0
    model = Item
    fk_name = 'item'
    raw_id_fields = ['type', 'product']
    readonly_fields = ['price', 'image_tag']
    classes = ['collapse']


class OrderItemInline(admin.TabularInline):
    extra = 0
    model = OrderProductItem
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'subtotal']


class OrderProductInline(admin.TabularInline):
    extra = 0
    model = OrderProduct
    inlines = [OrderItemInline]
    # classes = ['collapse']
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'subtotal', 'total_price']
