from django.shortcuts import render, get_object_or_404
from .models import Product
from reviews.models import Review
from categories.models import Category  # Add this import

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Better than Product.objects.get()
    reviews = Review.objects.filter(product=product)
    # Or use the related manager: reviews = product.reviews.all()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews
    })

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category, in_stock=True)
    return render(
        request,
        'products/category_detail.html',
        {'category': category, 'products': products}
    )