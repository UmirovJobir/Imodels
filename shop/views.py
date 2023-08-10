from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Product, Category
from .serializers import ProductSerializer


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', context={'products':products})

