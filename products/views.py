from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, Category  # Ensure models exist

# Homepage or intro view
def index(request):
    return render(request, 'products/index.html')

# List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# Single product detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

# List all brands
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'products/brand_list.html', {'brands': brands})

# Single brand detail with related products
def brand_detail(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    products = Product.objects.filter(brand=brand)
    return render(request, 'products/brand_detail.html', {
        'brand': brand,
        'products': products
    })

# List all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})
