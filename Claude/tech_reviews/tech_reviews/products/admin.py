from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image_tag', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'short_description')
    ordering = ('-created_at',)

    # Optional: display a thumbnail of the product image in the list view
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'
