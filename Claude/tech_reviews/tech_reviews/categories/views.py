from django.shortcuts import render, get_object_or_404
from .models import Category
from products.models import Product


def category_list(request):
    categories = Category.objects.all()
    return render(request, "categories/category_list.html", {
        "categories": categories
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, "categories/category_detail.html", {
        "category": category,
        "products": products
    })
