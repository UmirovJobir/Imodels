import nested_admin
from django.db import models
from tinymce.widgets import TinyMCE
from modeltranslation.admin import TranslationTabularInline
from .models import (
    Category,
    ProductImage,
    ProductVideo,
    Description,
    ExtraDescImage,
    ExtraDescription,
    ProductFeature,
    ProductFeatureOption,
)

class CategoryInline(TranslationTabularInline):
    extra = 0
    model = Category
    verbose_name = "Подкатегория"
    verbose_name_plural = "Подкатегории"


class ProductVideoInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ProductVideo


class ProductImageInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ProductImage


class ProductFeatureOptionsInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ProductFeatureOption


class ProductFeatureInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeatureOptionsInline]


class DescriptionInline(nested_admin.NestedTabularInline, TranslationTabularInline):
    extra = 0
    model = Description


class ExtraDescImageInline(nested_admin.NestedStackedInline):
    extra = 0
    model = ExtraDescImage


class ExtraDescriptionInline(nested_admin.NestedTabularInline, TranslationTabularInline):
    extra = 0
    model = ExtraDescription
    inlines = [ExtraDescImageInline, DescriptionInline]



