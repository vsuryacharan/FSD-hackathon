from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):  # Use the correct class name
    list_display = ['name', 'supplier', 'store', 'price', 'discount_pcnt']

# Register the model with the custom admin settings
admin.site.register(Product, ProductAdmin)
