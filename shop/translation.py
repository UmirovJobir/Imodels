from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Description, ExtraDescription


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['title', 'description']