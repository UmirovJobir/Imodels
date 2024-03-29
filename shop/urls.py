from django.urls import path
from .views import (
    ProductListAPIView,
    ProductRetrieveAPIView,
    CategoryView,
    SubCategoryView,
    BlogView,
    PopularBlogView,
    BlogDetailView,
    ContactRequestCreateView,
    CartView,
    OrderView,
    SaleView,
    BlogListView,
    BlogDetailesView,
    QuillPostListAPIView,
    QuillPostRetrieveAPIView,
    model_form_view
)

urlpatterns = [
    path('html/', model_form_view),

    path('quillpost/', QuillPostListAPIView.as_view(), name='quillposts'),
    path('quillpost/<int:pk>/', QuillPostRetrieveAPIView.as_view(), name='quillpost'),

    path('products/', ProductListAPIView.as_view(), name='products'),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product'),

    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/', SubCategoryView.as_view(), name='subcategories'),
    
    path('blog/', BlogView.as_view(), name='blogs'),
    path('blog-popular/', PopularBlogView.as_view(), name='popular-blogs'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog'),
    
    path('contact/', ContactRequestCreateView.as_view(), name='contact'),
    path('cart/', CartView.as_view(), name='cart'),

    path('order/', OrderView.as_view(), name='order'),

    path('sale/', SaleView.as_view(), name='sale'),

    path('blog-list/', BlogListView.as_view(), name='blog_list'),
    path('blog-list/<int:pk>/', BlogDetailesView.as_view(), name='blog_details'),
    ]