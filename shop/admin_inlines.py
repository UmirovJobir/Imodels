from nested_admin import NestedStackedInline, NestedTabularInline
from django import forms
from django.db import models
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


class ProductImageInline(NestedStackedInline):
    extra = 0
    model = ProductImage
    classes = ['collapse']


class ProductFeatureOptionsInline(NestedStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ProductFeatureOption


class ProductFeatureInline(NestedStackedInline):
    extra = 0
    model = ProductFeature
    inlines = [ProductFeatureOptionsInline]
    classes = ['collapse']



class DescriptionInline(NestedTabularInline, TranslationTabularInline):
    extra = 0
    model = Description


class ExtraDescImageInline(NestedStackedInline):
    extra = 0
    model = ExtraDescImage


class ExtraDescriptionInline(NestedStackedInline, TranslationStackedInline):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
    }
    extra = 0
    model = ExtraDescription
    inlines = [ExtraDescImageInline, DescriptionInline]
    classes = ['collapse']




