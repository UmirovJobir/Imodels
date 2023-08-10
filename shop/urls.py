from django.urls import path
from .views import ProductView, index


urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('index/', index, name='index')
]