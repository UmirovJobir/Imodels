from django.contrib import admin
from .models import Category


class CategoryFilter(admin.SimpleListFilter):
    title = 'Родительские категории'
    parameter_name = 'parent category'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in model_admin.model.objects.filter(parent__isnull=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__name=self.value())


class ProductFilter(admin.SimpleListFilter):
    title = 'Подкатегории'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in Category.objects.filter(parent__isnull=False)]

    def queryset(self, request, queryset):
        if self.value():
            print(queryset)
            return queryset.filter(category__name=self.value())