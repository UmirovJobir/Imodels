from modeltranslation.translator import register, TranslationOptions
from modeltranslation.utils import build_localized_fieldname
from django.conf import settings
from .models import (
    Category,
    Product,
    ProductVideo,
    ProductFeatureOption,
    ExtraDescription,
    Description,
    Blog
)


def get_full_value(obj, field: str):
    available_languages = [language[0] for language in settings.LANGUAGES]
    
    values_in_all_languages = {}

    for language in available_languages:
        field_name = build_localized_fieldname(field, language)
        translated_value = getattr(obj, field_name)
        values_in_all_languages[language] = translated_value
    
    return values_in_all_languages



@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


@register(ProductVideo)
class ProductVideoTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


@register(ProductFeatureOption)
class ProductFeatureOptionTranslationOptions(TranslationOptions):
    fields = ['feature']


@register(ExtraDescription)
class ExtraDescriptionTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Description)
class DescriptionTranslationOptions(TranslationOptions):
    fields = ['text']


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ['title', 'text']