from django.urls import path
from .views import (
    ProductView,
    CategoryView,
    SubCategoryView,
    BlogView,
    index, 
    upload_image
)


urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/', SubCategoryView.as_view(), name='categories'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('index/', index, name='index'),
]