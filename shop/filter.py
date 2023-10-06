from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    category_id = filters.NumberFilter(field_name='category__id', lookup_expr='exact')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category_id', 'title']