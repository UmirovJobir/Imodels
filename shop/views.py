from django.shortcuts import render
from django.utils import translation

from rest_framework.generics import ListAPIView

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


def get_query_by_heard(self, queryset):
    if 'HTTP_ACCEPT_LANGUAGE' in self.request.META:
        lang = self.request.META['HTTP_ACCEPT_LANGUAGE']
        translation.activate(lang)
    return queryset


class CategoryView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        return get_query_by_heard(self, queryset)
    

class ProductView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        return get_query_by_heard(self, queryset)



def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', context={'products':products})

