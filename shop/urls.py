from django.urls import path
from .views import (
    ProductListAPIView,
    ProductRetrieveAPIView,
    CategoryView,
    SubCategoryView,
    BlogView,
    ContactRequestCreateView,
    ConfiguratorAPIView,
    index
)


urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product'),
    path('products/<int:pk>/configurator/', ConfiguratorAPIView.as_view(), name='product'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/', SubCategoryView.as_view(), name='categories'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactRequestCreateView.as_view(), name='contact'),
    path('index/', index, name='index'),
]