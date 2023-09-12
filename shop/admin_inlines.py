from django import forms
from django.db import models
from django.contrib import admin
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
    Configurator,
    ConfiguratorCategory,
    ConfiguratorProduct,
    CartItem,
    OrderItem,
    OrderConfigurator,
    OrderConfiguratorItem,
)

class CategoryInline(TranslationTabularInline):
    extra = 0
    model = Category
    verbose_name = "Подкатегория"
    verbose_name_plural = "Подкатегории"


class ProductVideoInline(NestedStackedInline, TranslationStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductVideo
    classes = ['collapse']
    readonly_fields = ['video_tag']


class ProductImageInline(NestedTabularInline):
    extra = 0
    model = ProductImage
    classes = ['collapse']
    readonly_fields = ['image_tag']


class ProductFeatureOptionsInline(NestedStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductFeatureOption


class ProductFeatureInline(NestedTabularInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeatureOptionsInline]
    classes = ['collapse']
    readonly_fields = ['image_tag']


class DescriptionInline(NestedTabularInline, TranslationTabularInline):
    extra = 0
    model = Description


class ExtraDescImageInline(NestedTabularInline):
    extra = 0
    model = ExtraDescImage
    readonly_fields = ['image_tag']


class ExtraDescriptionInline(NestedStackedInline, TranslationStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ExtraDescription
    inlines = [ExtraDescImageInline, DescriptionInline]
    classes = ['collapse']


class ConfiguratorProductInline(NestedTabularInline):
    extra = 0
    model = ConfiguratorProduct
    readonly_fields = ['image_tag']


class ConfiguratorCategoryInline(NestedStackedInline):
    extra = 0
    model = ConfiguratorCategory
    inlines = [ConfiguratorProductInline]


class ConfiguratorInline(NestedTabularInline):
    extra = 0
    model = Configurator
    inlines = [ConfiguratorCategoryInline]
    classes = ['collapse']
    readonly_fields = ['image_tag']


class CartItemInline(admin.TabularInline):
    extra = 0
    model = CartItem


class OrderConfiguratorItemInline(NestedTabularInline):
    extra = 0
    model = OrderConfiguratorItem
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'subtotal']


class OrderConfiguratorInline(NestedTabularInline):
    extra = 0
    model = OrderConfigurator
    inlines = [OrderConfiguratorItemInline]
    raw_id_fields = ['configurator']
    readonly_fields = ['image_tag', 'subtotal', 'total_price']


class OrderItemInline(NestedTabularInline):
    extra = 0
    model = OrderItem
    inlines = [OrderConfiguratorInline]
    classes = ['collapse']
    raw_id_fields = ['product']
    readonly_fields = ['image_tag', 'subtotal', 'total_price']
