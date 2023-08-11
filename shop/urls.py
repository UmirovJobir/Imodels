from django.urls import path
from .views import (
    ProductView,
    CategoryView,
    SubCategoryView,
    index
)


urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/', SubCategoryView.as_view(), name='categories'),
    path('index/<int:pk>/', index, name='index')
]