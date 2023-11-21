"""imodels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [   
    path('backend/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('backend/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('backend/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('backend/admin/', admin.site.urls),
    path('backend/account/', include('account.urls')),
    path('backend/shop/', include('shop.urls')),

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('backend/summernote/', include('django_summernote.urls')),
    path('backend/__debug__/', include('debug_toolbar.urls')),
    path('backend/_nested_admin/', include('nested_admin.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += [re_path(r'^backend/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]