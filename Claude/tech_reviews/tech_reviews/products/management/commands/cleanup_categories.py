# Create this file: management/commands/cleanup_categories.py

from django.core.management.base import BaseCommand
from django.db.models import Count
from categories.models import Category
from products.models import Product

class Command(BaseCommand):
    help = 'Clean up duplicate categories and merge products'

    def handle(self, *args, **options):
        self.stdout.write("Starting category cleanup...")
        
        # Find categories with similar names (case-insensitive)
        all_categories = Category.objects.all()
        processed = set()
        merged_count = 0
        
        for category in all_categories:
            if category.id in processed:
                continue
                
            # Find similar categories (case-insensitive)
            similar_categories = Category.objects.filter(
                name__iexact=category.name
            ).exclude(id=category.id)
            
            if similar_categories.exists():
                self.stdout.write(f"Found duplicates for '{category.name}':")
                
                # Keep the first one, merge others into it
                main_category = category
                
                for duplicate in similar_categories:
                    self.stdout.write(f"  - Merging '{duplicate.name}' (ID: {duplicate.id}) into '{main_category.name}' (ID: {main_category.id})")
                    
                    # Move all products from duplicate to main category
                    products_moved = Product.objects.filter(category=duplicate).update(category=main_category)
                    self.stdout.write(f"    Moved {products_moved} products")
                    
                    # Mark as processed
                    processed.add(duplicate.id)
                    
                    # Delete duplicate
                    duplicate.delete()
                    merged_count += 1
                
                processed.add(main_category.id)
        
        self.stdout.write(self.style.SUCCESS(f"Cleanup complete! Merged {merged_count} duplicate categories."))
        
        # Show final category list
        self.stdout.write("\nFinal categories:")
        for cat in Category.objects.all().order_by('name'):
            product_count = Product.objects.filter(category=cat).count()
            self.stdout.write(f"  - {cat.name} ({product_count} products)")