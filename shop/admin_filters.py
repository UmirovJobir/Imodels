from django.contrib import admin


class CategoryFilter(admin.SimpleListFilter):
    title = 'Родительские категории'
    parameter_name = 'subcategory'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in model_admin.model.objects.filter(parent__isnull=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__name=self.value())