from django.contrib import admin
from .models import Review  # Import from the same app
# Or alternatively: from reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['title', 'comment', 'user__username', 'product__name']
    readonly_fields = ['created_at']