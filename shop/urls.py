from django.urls import path
from .views import (
    ProductView,
    CategoryView,
    SubCategoryView,
    BlogView,
    ContactRequestCreateView,
    ConfiguratorListView,
    index
)


urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('subcategories/', SubCategoryView.as_view(), name='categories'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactRequestCreateView.as_view(), name='contact'),
    path('configurator/', ConfiguratorListView.as_view(), name='configurator'),
    path('index/', index, name='index'),
]