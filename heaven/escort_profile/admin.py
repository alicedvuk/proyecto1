from django.contrib import admin
from .models import Category, Escort


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Escort)
class EscortProfileAdmin(admin.ModelAdmin):
    list_display = ('verbose_name', 'name', 'popular', 'featured', 'created')
    list_filter = ( 'popular', 'featured', 'created')

    date_hierarchy = 'created'