from django.contrib import admin
from .models import Category


class CategoryFilter(admin.SimpleListFilter):
    title = 'Bosh kategoriyalar'
    parameter_name = 'parent_category'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in model_admin.model.objects.filter(parent__isnull=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__name=self.value())


class ProductFilter(admin.SimpleListFilter):
    title = 'Kategoriyalar'
    parameter_name = 'subcategory'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in Category.objects.filter(parent__isnull=False)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__name=self.value())
        
    # def lookups(self, request, model_admin):
    #     return [(i.name, i.name) for i in Category.objects.all()] #.filter(parent__isnull=False)]

    # def queryset(self, request, queryset):
    #     if self.value():
    #         query = queryset.filter(category__name=self.value())
    #         if len(query)==0:
    #             category = Category.objects.get(name=self.value())

    #             subcategories = category.subcategories.all()

    #             query = queryset.filter(category__in=subcategories)

    #         return query