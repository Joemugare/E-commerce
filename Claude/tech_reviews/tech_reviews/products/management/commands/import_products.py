# =====================================================
# 1. UPDATED IMPORT SCRIPT (management/commands/import_products.py)
# =====================================================

import os
import re
import json
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from products.models import Product
from categories.models import Category
from urllib.parse import urlparse
from io import BytesIO

class Command(BaseCommand):
    help = 'Imports products from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        try:
            with open(json_file, 'r', encoding="utf-8") as file:
                data = json.load(file)

                # Extract products
                if isinstance(data, dict) and 'products' in data:
                    products = data['products']
                elif isinstance(data, list):
                    products = data
                else:
                    self.stdout.write(self.style.ERROR(f"Unexpected JSON structure: {type(data)}"))
                    return

                if not products:
                    self.stdout.write(self.style.WARNING("No products found in JSON"))
                    return

                for product_data in products:
                    if not isinstance(product_data, dict):
                        self.stdout.write(self.style.WARNING(
                            f"Skipping invalid product entry: {product_data}"
                        ))
                        continue

                    # Name
                    name = product_data.get('title') or product_data.get('name', '')
                    if not name:
                        self.stdout.write(self.style.WARNING("Missing name/title, skipping"))
                        continue

                    # ✅ Enhanced Category detection with duplicate prevention
                    category_name = self.extract_category(product_data)
                    category = self.get_or_create_category(category_name)

                    # Price
                    price_str = product_data.get('price', '0')
                    try:
                        price = float(re.sub(r'[^\d.]', '', price_str))
                    except ValueError:
                        price = 0.0

                    # Handle image
                    image_url = product_data.get('image_url')
                    if image_url:
                        self.handle_with_image(name, product_data, category, price, image_url)
                    else:
                        self.create_product_without_image(name, product_data, category, price)

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {json_file} not found"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))

    def get_or_create_category(self, category_name):
        """Get or create category with duplicate prevention"""
        try:
            # Try case-insensitive lookup first
            category = Category.objects.filter(name__iexact=category_name).first()
            if category:
                return category
            
            # If not found, create new one
            category, created = Category.objects.get_or_create(
                name__iexact=category_name,
                defaults={'name': category_name}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category_name}"))
            
            return category
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Error with category {category_name}: {str(e)}"))
            # Fallback to Miscellaneous
            category, _ = Category.objects.get_or_create(name="Miscellaneous")
            return category

    def extract_category(self, product_data):
        """Extract and normalize category from product data"""
        
        # First check if category is directly provided
        category_name = product_data.get('category')
        if category_name:
            return self.normalize_category(category_name)
        
        # Extract from key_features
        key_features = product_data.get('key_features', [])
        
        # Look for various category indicators in key_features
        category_indicators = [
            'Type:', 'Form Factor:', 'Category:', 'Product Type:', 
            'Device Type:', 'Item Type:'
        ]
        
        for feature in key_features:
            if isinstance(feature, str):
                for indicator in category_indicators:
                    if feature.startswith(indicator):
                        raw_category = feature.split(':', 1)[1].strip()
                        return self.normalize_category(raw_category)
        
        # Fallback: try to detect category from title
        title = product_data.get('title', '').lower()
        category_from_title = self.detect_category_from_title(title)
        if category_from_title:
            return category_from_title
        
        return "Miscellaneous"

    def normalize_category(self, raw_category):
        """Normalize category names to standard format"""
        if not raw_category:
            return "Miscellaneous"
        
        raw_category = raw_category.strip().lower()
        
        # Category mapping for normalization
        category_mapping = {
            # Phones
            'smart phones': 'Smartphones',
            'smartphone': 'Smartphones',
            'phone': 'Smartphones',
            'mobile phone': 'Smartphones',
            'cell phone': 'Smartphones',
            'cellular phone': 'Smartphones',
            
            # Audio
            'headphones': 'Headphones',
            'earphones': 'Headphones',
            'earbuds': 'Headphones',
            'headset': 'Headphones',
            'speakers': 'Speakers',
            'audio': 'Audio Equipment',
            
            # TV & Displays
            'tv': 'TVs',
            'television': 'TVs',
            'monitor': 'Monitors',
            'display': 'Displays',
            
            # Computers
            'laptop': 'Laptops',
            'notebook': 'Laptops',
            'desktop': 'Desktops',
            'computer': 'Computers',
            'pc': 'Computers',
            
            # Gaming
            'gaming': 'Gaming',
            'console': 'Gaming Consoles',
            'xbox': 'Gaming Consoles',
            'playstation': 'Gaming Consoles',
            'nintendo': 'Gaming Consoles',
            
            # Accessories
            'case': 'Accessories',
            'cover': 'Accessories',
            'charger': 'Accessories',
            'cable': 'Accessories',
            'adapter': 'Accessories',
            
            # Tablets
            'tablet': 'Tablets',
            'ipad': 'Tablets',
            
            # Wearables
            'watch': 'Wearables',
            'smartwatch': 'Wearables',
            'fitness tracker': 'Wearables',
        }
        
        # Direct match
        if raw_category in category_mapping:
            return category_mapping[raw_category]
        
        # Partial match
        for key, value in category_mapping.items():
            if key in raw_category:
                return value
        
        # If no match found, capitalize the first letter of each word
        return ' '.join(word.capitalize() for word in raw_category.split())

    def detect_category_from_title(self, title_lower):
        """Detect category from product title as fallback"""
        
        title_keywords = {
            'Smartphones': ['smartphone', 'phone', 'iphone', 'galaxy', 'pixel'],
            'Headphones': ['headphone', 'earphone', 'earbud', 'headset'],
            'TVs': ['tv', 'television', 'smart tv'],
            'Laptops': ['laptop', 'notebook', 'macbook'],
            'Tablets': ['tablet', 'ipad'],
            'Wearables': ['watch', 'smartwatch'],
            'Speakers': ['speaker', 'bluetooth speaker'],
            'Gaming': ['gaming', 'xbox', 'playstation', 'nintendo'],
        }
        
        for category, keywords in title_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return None

    def handle_with_image(self, name, product_data, category, price, image_url):
        key_features = product_data.get('key_features', [])
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path) or f"product_{abs(hash(name))}.jpg"
                image_file = File(BytesIO(response.content), name=filename)

                product, _ = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        'short_description': ' '.join(key_features) if key_features else 'No description available',
                        'price': price,
                        'category': category,
                        'in_stock': product_data.get('in_stock', True),
                    }
                )
                product.image.save(filename, image_file, save=True)
                self.stdout.write(self.style.SUCCESS(f"Imported/Updated product with image: {name} -> {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Failed to download image for {name}"))
                self.create_product_without_image(name, product_data, category, price)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Error downloading image for {name}: {str(e)}"))
            self.create_product_without_image(name, product_data, category, price)

    def create_product_without_image(self, name, product_data, category, price):
        key_features = product_data.get('key_features', [])
        try:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    'short_description': ' '.join(key_features) if key_features else 'No description available',
                    'price': price,
                    'category': category,
                    'in_stock': product_data.get('in_stock', True),
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Imported/Updated product (no image): {name} -> {category.name}"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Error saving {name}: {str(e)}"))


# =====================================================
# 2. UPDATED CATEGORY VIEW (categories/views.py)
# =====================================================

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from categories.models import Category
from products.models import Product

def category_list(request):
    """Display products filtered by category"""
    
    # Get category parameter from URL
    category_slug = request.GET.get('category', '').strip()
    
    if category_slug:
        try:
            # Use case-insensitive lookup and get first match to avoid MultipleObjectsReturned
            category = Category.objects.filter(name__iexact=category_slug).first()
            
            if not category:
                # If no exact match, try contains search
                category = Category.objects.filter(name__icontains=category_slug).first()
            
            if category:
                products = Product.objects.filter(category=category, in_stock=True)
                page_title = f"{category.name} Products"
            else:
                products = Product.objects.filter(in_stock=True)
                page_title = "All Products"
                
        except Exception as e:
            # Fallback to all products if there's any error
            products = Product.objects.filter(in_stock=True)
            page_title = "All Products"
    else:
        # Show all products if no category specified
        products = Product.objects.filter(in_stock=True)
        page_title = "All Products"
    
    # Get all categories for the sidebar/navigation
    categories = Category.objects.all().order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': categories,
        'current_category': category if 'category' in locals() else None,
        'page_title': page_title,
        'total_products': products.count(),
    }
    
    return render(request, 'categories/category_list.html', context)