import os
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.utils import translation
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.views import APIView
from rest_framework import filters, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
)
from . import api
# from .cart import Cart
from .cart_1 import Cart
from .filter import ProductFilter
from .pagination import CustomPageNumberPagination
from .models import (
    Category,
    Product,
    Blog,
    ContactRequest,
    Order,
    OrderProduct,
    OrderProductItem,
)
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    BlogListSerializer,
    BlogDetailSerializer,
    ContactRequestSerializer,
    OrderSerializer,
    CartProductSerilaizer
)


# @csrf_exempt
# def upload_image(request):
#     if request.method == "POST":
#         file_obj = request.FILES['file']
#         file_name_suffix = file_obj.name.split(".")[-1]
#         if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
#             return JsonResponse({"message": "Wrong file format"})

#         upload_time = timezone.now()
#         path = os.path.join(
#             settings.MEDIA_ROOT,
#             'tinymce',
#             str(upload_time.year),
#             str(upload_time.month),
#             str(upload_time.day)
#         )
#         # If there is no such path, create
#         if not os.path.exists(path):
#             os.makedirs(path)

#         file_path = os.path.join(path, file_obj.name)

#         file_url = f'{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

#         if os.path.exists(file_path):
#             return JsonResponse({
#                 "message": "file already exist",
#                 'location': file_url
#             })

#         with open(file_path, 'wb+') as f:
#             for chunk in file_obj.chunks():
#                 f.write(chunk)

#         return JsonResponse({
#             'message': 'Image uploaded successfully',
#             'location': file_url
#         })
#     return JsonResponse({'detail': "Wrong request"})


# def get_query_by_heard(self, queryset):
#     if 'HTTP_ACCEPT_LANGUAGE' in self.request.META:
#         lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE')
#         translation.activate(lang)
#     return queryset


# View related to Category
@extend_schema(
    tags=["Category"]
)
class CategoryView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True)
        return queryset

@extend_schema(
    tags=["Category"],
    parameters=[
        OpenApiParameter(
            name="accept-language",
            type=str,
            location=OpenApiParameter.HEADER,
            description="`uz` or `ru` or `en`. The default value is uz",
        ),
    ],
)
class SubCategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = SubCategorySerializer


# View related to Product
@extend_schema(
    tags=["Product"],
    parameters=[
        OpenApiParameter(
            name="category_id",
            type=int,
            location=OpenApiParameter.QUERY,
        ),
        # OpenApiParameter(
        #     name="currency",
        #     type=str,
        #     location=OpenApiParameter.HEADER,
        #     description="`usd` or `eur` or `uzs`. The default value is usd",
        # ),
    ],
)
class ProductListAPIView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(status="Visible").select_related('category', 'set_creator').order_by('order_by')
        category_id = self.request.query_params.get('category_id')
        if category_id:
            category = Category.objects.get(id=category_id)
            if category.products.all():
                return category.products.all()
            else:
                if category.subcategories.all():
                    return queryset.filter(category__in=category.subcategories.all())
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.context['request'] = self.request
        return serializer


@extend_schema(
    tags=["Product"],
    # parameters=[
    #     OpenApiParameter(
    #         name="accept-language",
    #         type=str,
    #         location=OpenApiParameter.HEADER,
    #         description="`uz` or `ru` or `en`. The default value is uz",
    #     ),
    #     OpenApiParameter(
    #         name="currency",
    #         type=str,
    #         location=OpenApiParameter.HEADER,
    #         description="`usd` or `eur` or `uzs`. The default value is usd",
    #     ),
    # ],
)
class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all().select_related('category', 'set_creator').order_by('order_by')
        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.context['request'] = self.request
        return serializer


# View related to Blog
@extend_schema(
    tags=["Blog"],
)
class BlogView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    pagination_class = CustomPageNumberPagination
    

@extend_schema(
    tags=["Blog"],
    responses=BlogDetailSerializer
)
class BlogDetailView(RetrieveAPIView):
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogDetailSerializer


# View related to ContactRequest
@extend_schema(tags=["Contact"])
class ContactRequestCreateView(CreateAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer


# View related to Cart
@extend_schema(
    tags=["Cart"]
)
class CartView(APIView):
    def request_cart(self):

        product_list = []
        total_cost = 0
        cart = Cart(self.request)

        for cart_product in cart.cart:
            product_queryset = Product.objects.select_related('category', 'set_creator').get(id=cart_product['id'])
            product =  product_queryset
            product_dict = {
                "id": product.pk,
                "price": product.price if product.price!=None else 0, #api.get_currency(obj_price=product.price) if product.price!=None else 0,
                "title": product.title,
                "image": self.request.build_absolute_uri(product.product_images.all().first().image.url),
                "quantity": cart_product['quantity']}
            total_cost += product_dict['price']

            if cart_product.get('items'):
                item_list = []
                for items in cart_product.get('items'):
                    item_queryset = Product.objects.select_related('category', 'set_creator').get(id=items['id'])
                    item =  item_queryset
                    items = {
                        "id": item.pk,
                        "price": item.price, # if item.price!=None else 0,
                        "title": item.title,
                        "image": self.request.build_absolute_uri(item.product_images.all().first().image.url),
                        "quantity": items['quantity'] * cart_product['quantity']}
                    item_list.append(items)
                    print(items['price'], items['quantity'])
                    # total_cost += items['price'] * items['quantity']

                product_dict['items'] = item_list
            product_list.append(product_dict)
        data = {"products": product_list, "total_cost":total_cost}
        return data


    @extend_schema(
        tags=["Cart"],
        responses=CartProductSerilaizer,
    )
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        data = list(cart.__iter__(request))
        return Response(
            {"data": data, 
            "cart_total_price": cart.get_total_price(data)
            },
            status=status.HTTP_200_OK
            )


    @extend_schema(
            tags=["Cart"],
            request=CartProductSerilaizer,
            responses=CartProductSerilaizer,
    )
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = request.data
        cart.add(
                product=product["product"],
                quantity=product["quantity"],
                items = product['items'] if 'items' in product else [],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )
        return Response({"message": "cart updated"}, status=status.HTTP_202_ACCEPTED)


    @extend_schema(
        tags=["Cart"]
    )
    def delete(self, request):
        cart = Cart(request)
        
        product = request.data.get("product")
        quantity = request.data.get("quantity")

        if quantity==None:
            cart.remove(product)
            return Response({"detail": "product removed"}, status=status.HTTP_202_ACCEPTED)

        keys_to_remove = []

        for cart_product, value in cart.cart.items():
            if cart_product==str(product):
                if value['quantity']==quantity or value['quantity'] <= 1:
                    keys_to_remove.append(str(product))
                else:
                    value['quantity'] -= 1

        if len(keys_to_remove) > 0:
            for key in keys_to_remove:
                cart.remove(key)
        cart.save()
        return Response({"detail": "cart updated"}, status=status.HTTP_202_ACCEPTED)


@extend_schema(
    tags=["Order"],
    request=OrderSerializer,
    responses=OrderSerializer,
)
class OrderView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer'] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)



    # def create(self, request, *args, **kwargs):
    #     # Deserialize the request data using the OrderSerializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     # Create Order instance
    #     order = serializer.save()

    #     # Create OrderProducts and OrderItems
    #     order_products_data = serializer.validated_data.pop('order_products')
    #     for order_product_data in order_products_data:
    #         order_items_data = order_product_data.pop('order_items')
    #         order_product = OrderProduct.objects.create(order=order, **order_product_data)
    #         for order_item_data in order_items_data:
    #             OrderProductItem.objects.create(order_product=order_product, **order_item_data)

    #     return Response(OrderSerializer(order, many=True).data, status=status.HTTP_201_CREATED)

