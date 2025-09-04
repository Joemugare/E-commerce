# products/management/commands/generate_small_images.py
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Generate small images for existing products'

    def handle(self, *args, **kwargs):
        for product in Product.objects.filter(image__isnull=False):
            if not product.image_small:
                try:
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f"Generated small image for {product.name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error for {product.name}: {e}"))