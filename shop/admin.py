from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'parent', 'name'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_fields = 'title', 'price'

