from django.db import transaction
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework import filters, status, permissions
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
)
from .cart import Cart
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
    ],
)
class ProductListAPIView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(status="Visible") \
            .order_by('order_by') \
            .prefetch_related('product_images', 'item', 'items') \
            .select_related('category', 'configurator', 'product_video', 'product_features', 'product_description')

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
)
class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all() \
            .order_by('order_by') \
            .prefetch_related('product_images', 'item','items') \
            .select_related('category', 'configurator', 'product_video', 'product_features', 'product_description')
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
    queryset = Blog.objects.all().order_by("-created_at")
    serializer_class = BlogListSerializer
    pagination_class = CustomPageNumberPagination

@extend_schema(
    tags=["Blog"],
)
class PopularBlogView(ListAPIView):
    queryset = Blog.objects.filter(popular=True).order_by("-created_at")
    serializer_class = BlogListSerializer
    pagination_class = CustomPageNumberPagination


@extend_schema(
    tags=["Blog"],
    responses=BlogDetailSerializer
)
class BlogDetailView(RetrieveAPIView):
    queryset = Blog.objects.all()
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
    @extend_schema(
        tags=["Cart"],
        responses=CartProductSerilaizer,
    )
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        data = list(cart.__iter__(request))
        return Response({
            "data": data, 
            "cart_total_price": cart.get_total_price(data)
            }, status=status.HTTP_200_OK)


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
        return Response({"detail": "cart updated"}, status=status.HTTP_202_ACCEPTED)


    @extend_schema(
        tags=["Cart"],
        description="Delete a product with quantity from the cart by ID.",
        parameters=[
            OpenApiParameter(
                name="product",
                type=int,
                location=OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                name="quantity",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False
            ),
        ],
    )
    def delete(self, request):
        cart = Cart(request)
        
        product = request.GET.get("product")
        quantity = request.GET.get("quantity")

        if product==None:
            return Response({"error": "product is not given"})

        if quantity==None:
            cart.remove(product)
            return Response({"detail": "product removed"}, status=status.HTTP_202_ACCEPTED)

        keys_to_remove = []

        if str(product) not in cart.cart.keys():
            return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)

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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = Order.objects.create(customer=request.user)
        for product in request.data:
            order_product = OrderProduct.objects.create(
                    order=order,
                    quantity     = product['quantity'],
                    product      = get_object_or_404(Product, pk=product['product']),
                    configurator = get_object_or_404(Product, pk=product['configurator']) if 'configurator' in product else None,
                    price        = product['price']['uzs'] if product['price']!=None else None,
                    price_usd    = product['price']['usd'] if product['price']!=None else None,
                    price_eur    = product['price']['eur'] if product['price']!=None else None)
            
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class OrderCreate(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
        
#         order = Order.objects.create(customer=request.user)
#         for product in request.data:

#             order_product = OrderProduct.objects.create(
#                     order=order,
#                     quantity  = product['quantity'],
#                     product   = get_object_or_404(Product, pk=product['product']),
#                     price     = product['price']['uzs'] if product['price']!=None else None,
#                     price_usd = product['price']['usd'] if product['price']!=None else None,
#                     price_eur = product['price']['eur'] if product['price']!=None else None)

#             if product.get('main_item'):
#                 product_price = product['main_item']['price']
#                 order_item = OrderProductItem.objects.create(
#                                 order_product = order_product,
#                                 quantity      = product['main_item']['quantity'],
#                                 product       = get_object_or_404(Product, pk=product['main_item']['product']),
#                                 price         = product_price['uzs'] if product_price['uzs']!=None else None,
#                                 price_usd     = product_price['usd'] if product_price['usd']!=None else None,
#                                 price_eur     = product_price['eur'] if product_price['eur']!=None else None)
            
#             if product.get('order_items'):
#                 for item in product['order_items']:
#                     item_price = item['price']
#                     order_item = OrderProductItem.objects.create(
#                             order_product = order_product,
#                             quantity      = item['quantity'],
#                             product       = get_object_or_404(Product, pk=item['product']),
#                             price         = item_price['uzs'] if item_price['uzs']!=None else None,
#                             price_usd     = item_price['usd'] if item_price['usd']!=None else None,
#                             price_eur     = item_price['eur'] if item_price['eur']!=None else None)
            
#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_200_OK)





def index(request):
    blog = Blog.objects.get(id=2)
    return render(request, 'blog.html', context={'blog':blog})