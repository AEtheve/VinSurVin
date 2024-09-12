from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'type', 'millesime')
    search_fields = ('name', 'producer', 'domain')
    list_filter = ('type', 'millesime')

admin.site.register(Product, ProductAdmin)