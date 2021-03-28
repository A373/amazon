from django.contrib import admin
from .models import Category, Product


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
    list_filter = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'price', 'image', 'description']
    list_filter = ['category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)