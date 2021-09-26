from django.contrib import admin
from .models import SiteConfig
# from django.contrib.sites.models import Site

# Register your models here.


@admin.register(SiteConfig)
class SiteAConfigadmin(admin.ModelAdmin):
    list_display = ('id', 'meta_title',)
    list_display_links = ('meta_title',)
