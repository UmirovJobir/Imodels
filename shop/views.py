from django.shortcuts import render
from django.utils import translation

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import (
    Category,
    Product
)
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductListSerializer,
)


def get_query_by_heard(self, queryset):
    if 'HTTP_ACCEPT_LANGUAGE' in self.request.META:
        lang = self.request.META['HTTP_ACCEPT_LANGUAGE']
        translation.activate(lang)
    return queryset


class CategoryView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True)
        return get_query_by_heard(self, queryset)


class SubCategoryView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=False)
        return get_query_by_heard(self, queryset)


class ProductView(ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category']
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all().select_related('category')
        return get_query_by_heard(self, queryset)







def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', context={'products':products})

