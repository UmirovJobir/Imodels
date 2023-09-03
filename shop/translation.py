from modeltranslation.translator import register, TranslationOptions
from .models import (
    Category,
    Product,
    ExtraDescription,
    Description,
    Blog
)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


@register(ExtraDescription)
class ExtraDescriptionTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Description)
class DescriptionTranslationOptions(TranslationOptions):
    fields = ['text']


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ['title', 'text']