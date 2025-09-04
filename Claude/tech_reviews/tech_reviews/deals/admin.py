from django.contrib import admin
from django import forms
from .models import Deal
from urllib.parse import urlparse, parse_qs
import requests
from django.core.files.base import ContentFile
import os

class DealAdminForm(forms.ModelForm):
    image_url = forms.URLField(
        required=False,
        help_text="Enter an image URL to download (e.g., https://example.com/image.jpg), or upload an image file below."
    )

    class Meta:
        model = Deal
        fields = '__all__'

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    form = DealAdminForm
    list_display = ('title', 'discount_percentage', 'deal_price', 'link', 'is_affiliate_link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    list_editable = ('discount_percentage', 'deal_price', 'link')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image_url', 'image')
        }),
        ('Pricing', {
            'fields': ('discount_percentage', 'original_price', 'deal_price')
        }),
        ('Affiliate Link', {
            'fields': ('link',)
        }),
    )
    readonly_fields = ('created_at',)

    def is_affiliate_link(self, obj):
        if not obj.link:
            return False
        parsed_url = urlparse(obj.link)
        query_params = parse_qs(parsed_url.query)
        affiliate_indicators = ['tag', 'aff_id', 'affiliate', 'u', 'b']
        return any(param in query_params for param in affiliate_indicators)
    
    is_affiliate_link.short_description = 'Affiliate Link?'
    is_affiliate_link.boolean = True

    def save_model(self, request, obj, form, change):
        # Handle image URL if provided
        image_url = form.cleaned_data.get('image_url')
        if image_url:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    filename = os.path.basename(urlparse(image_url).path) or 'deal_image.jpg'
                    obj.image.save(filename, ContentFile(response.content), save=False)
                else:
                    self.message_user(request, f"Failed to download image from {image_url}. Please upload an image file manually.", level='error')
                    obj.image = None
            except Exception as e:
                self.message_user(request, f"Error downloading image: {str(e)}. Please upload an image file manually.", level='error')
                obj.image = None

        # Handle file upload (if provided)
        if form.cleaned_data.get('image'):
            obj.image = form.cleaned_data['image']

        # Handle affiliate link
        if obj.link:
            if not obj.link.startswith(('http://', 'https://')):
                obj.link = f'https://{obj.link}'
            if 'amazon.com' in obj.link and 'tag=' not in obj.link:
                affiliate_id = 'your_affiliate_id'  # Replace with your actual affiliate ID
                obj.link = f"{obj.link}?tag={affiliate_id}"
        super().save_model(request, obj, form, change)