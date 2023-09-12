import os
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.utils import translation
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from .cart import Cart
from .filter import ProductFilter
from .pagination import CustomPageNumberPagination
from .models import (
    Category,
    Product,
    Blog,
    ContactRequest,
    Configurator
)
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductListSerializer,
    BlogSerializer,
    ContactRequestSerializer,
    ConfiguratorProductNotPriceSerializer
)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})


def get_query_by_heard(self, queryset):
    if 'HTTP_ACCEPT_LANGUAGE' in self.request.META:
        lang = self.request.META['HTTP_ACCEPT_LANGUAGE']
        translation.activate(lang)
    return queryset


# View related to Category
class CategoryView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True)
        return get_query_by_heard(self, queryset)


class SubCategoryView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        print(Configurator.objects.all())
        queryset = Category.objects.all()
        return get_query_by_heard(self, queryset)


# View related to Product
class ProductListAPIView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all().select_related('category')
        return get_query_by_heard(self, queryset)


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all().select_related('category')
        return get_query_by_heard(self, queryset)


# View related to Blog
class BlogView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = BlogSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Blog.objects.all()
        return get_query_by_heard(self, queryset)


# View related to ContactRequest
class ContactRequestCreateView(CreateAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer


#View related to Configurator
class ConfiguratorAPIView(APIView):
    def get(self, request):
        configurators = Configurator.objects.all()
        products = [configurator.product for configurator in configurators]
        serializer = ConfiguratorProductNotPriceSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', context={'products':products})


class CartView(APIView):
    def request_cart(self):
        data_list = []
        total_cost = 0
        cart = Cart(self.request)
        for item in cart.cart:
            product = Product.objects.select_related('category', 'related_configurator').get(id=item['id'])
            data = {
                "id": product.pk,
                "price": product.price,
                "title": product.title,
                "image": self.request.build_absolute_uri(product.product_images.all().first().image.url),
                "quantity": item['quantity'],
            }
            total_cost += product.price
            if item.get('configurators'):
                conf_list = []
                if product.configurator:
                    conf = {
                        "id": product.configurator.pk,
                        "price": product.configurator.price,
                        "title": product.configurator.conf_title,
                        "image": self.request.build_absolute_uri(product.configurator.conf_image.url),
                        "quantity":  item['quantity'],
                    }
                    conf_list.append(conf)
                    total_cost += product.configurator.price
                for configurator in item.get('configurators'):
                    conf_product = Product.objects.select_related('category', 'related_configurator').get(id=configurator['id'])
                    configurators = {
                        "id": conf_product.pk,
                        "price": conf_product.price,
                        "title": conf_product.title,
                        "image": self.request.build_absolute_uri(conf_product.product_images.all().first().image.url),
                        "quantity": configurator['quantity'] * item['quantity'],
                    }
                    conf_list.append(configurators)
                    total_cost += conf_product.price
                data['configurators'] = conf_list
            data_list.append(data)
            data_list.append({"total_cost":total_cost})
        return data_list


    def get(self, request, *args, **kwargs):
        return Response(self.request_cart(), status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        data = request.data
        product = get_object_or_404(Product, id=data['id'])
        
        if data['id'] in [item['id'] for item in cart.cart]:
            for item in cart.cart:
                if item['id']==data['id']:
                    item['quantity'] += data['quantity']
        else:
            if request.data.get("configurators")==None:
                cart.add(product=product, quantity=data['quantity'])
            else:
                cart.add(product=product, quantity=data['quantity'], configurators=request.data.get("configurators"))
        cart.save()
        return Response(self.request_cart(), status=status.HTTP_200_OK)


    def delete(self, request):
        cart = Cart(request)
        if request.data['id'] not in [item['id'] for item in cart.cart]:
            return Response({"error": "id does not exist in Cart"}, status=status.HTTP_404_NOT_FOUND)
        
        product = get_object_or_404(Product, id=request.data['id'])

        for item in cart.cart:
            if item['id']==request.data['id']:
                if item['quantity']==request.data['quantity'] or item['quantity']==request.data['quantity'] <= 1:
                    cart.remove(product)
                else:
                    item['quantity'] -= 1
            cart.save()
        return Response(self.request_cart(), status=status.HTTP_200_OK)


