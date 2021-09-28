"""sortd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from sortd.swagger import schema_view
from seo.sitemaps import SITEMAPS


api_urls = [
    path('', include('shop.urls')),
    path('seo/', include('seo.urls')),
    path('info/', include('info.urls')),
    path('blogs/', include('blogs.urls')),
    path('users/', include('users.urls')),
    path('payment/', include('payment.urls')),
]

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    # path('jet/', include('jet.urls', 'jet')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/v1/', include(api_urls)),
]

# STATIC
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
