from django.contrib import admin
from .models import (
    SORTDSEO, ServiceSEO, AboutUsSEO, FAQSEO, ProductSEO, AnalyticMetric,
)


@admin.register(SORTDSEO)
class SORTDSEOAdmin(admin.ModelAdmin):
    list_display = ('seo_title',)


@admin.register(AboutUsSEO)
class AboutUsSEOAdmin(admin.ModelAdmin):
    list_display = ('seo_title',)


@admin.register(FAQSEO)
class FAQSEOAdmin(admin.ModelAdmin):
    list_display = ('seo_title',)


@admin.register(ServiceSEO)
class ServiceSEOAdmin(admin.ModelAdmin):
    list_display = ('seo_title',)


@admin.register(ProductSEO)
class ProductSEOAdmin(admin.ModelAdmin):
    list_display = ('seo_title',)


@admin.register(AnalyticMetric)
class AnalyticMetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_block_choice',)
    list_display_links = ('id', 'title',)
