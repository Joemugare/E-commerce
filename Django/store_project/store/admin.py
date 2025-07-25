from django.contrib import admin
from .models import Product, Price, MpesaPayment, StripePayment

class PriceInline(admin.TabularInline):
    model = Price
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'description')
    search_fields = ('name', 'description')
    list_filter = ('quantity',)
    fields = ('name', 'description', 'thumbnail', 'quantity')
    inlines = [PriceInline]

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_price', 'stripe_price_id')
    search_fields = ('product__name',)
    list_filter = ('product',)
    fields = ('product', 'price', 'stripe_price_id')

    def display_price(self, obj):
        return f"KSH {obj.price}"
    display_price.short_description = 'Price'

@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'phone_number', 'status', 'transaction_id', 'created_at')
    search_fields = ('phone_number', 'transaction_id')
    list_filter = ('status',)

@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'status', 'stripe_session_id', 'created_at')
    search_fields = ('stripe_session_id',)
    list_filter = ('status',)