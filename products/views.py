from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Product, Brand, Category

def get_common_context(request):
    cart = request.session.get('cart', {})
    cart_items = [item for item in cart.values() if isinstance(item, dict)]
    return {
        'categories': Category.objects.all(),
        'cart_item_count': sum(item.get('quantity', 0) for item in cart_items),
        'cart_total': sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items),
        'cart_items': cart_items,
    }

def index(request):
    featured_products = Product.objects.all()[:4]
    context = get_common_context(request)
    context.update({'featured_products': featured_products})
    return render(request, 'products/index.html', context)

def product_list(request):
    category_id = request.GET.get('category')
    sort = request.GET.get('sort', 'default')
    show = request.GET.get('show', '24')

    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    if sort == 'price':
        products = products.order_by('price')
    elif sort == 'name':
        products = products.order_by('name')

    try:
        per_page = int(show)
    except ValueError:
        per_page = 24

    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = get_common_context(request)
    context.update({
        'products': page_obj,
        'page_obj': page_obj,
    })
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = get_common_context(request)
    context.update({'product': product})
    return render(request, 'products/product_detail.html', context)

def brand_list(request):
    sort = request.GET.get('sort', 'default')
    show = request.GET.get('show', '12')
    brands = Brand.objects.all()

    if sort == 'name':
        brands = brands.order_by('name')

    try:
        per_page = int(show)
    except ValueError:
        per_page = 12

    paginator = Paginator(brands, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = get_common_context(request)
    context.update({
        'brands': page_obj,
        'page_obj': page_obj,
    })
    return render(request, 'products/brand_list.html', context)

def brand_detail(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    products = Product.objects.filter(brand=brand)
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = get_common_context(request)
    context.update({
        'brand': brand,
        'products': page_obj,
        'page_obj': page_obj,
    })
    return render(request, 'products/brand_detail.html', context)

def category_list(request):
    sort = request.GET.get('sort', 'default')
    show = request.GET.get('show', '12')
    categories = Category.objects.all()

    if sort == 'name':
        categories = categories.order_by('name')

    try:
        per_page = int(show)
    except ValueError:
        per_page = 12

    paginator = Paginator(categories, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = get_common_context(request)
    context.update({
        'categories': page_obj,
        'page_obj': page_obj,
    })
    return render(request, 'products/category_list.html', context)

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    item = cart.get(str(pk))
    if item and isinstance(item, dict):
        item['quantity'] += 1
    else:
        cart[str(pk)] = {
            'id': pk,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '/static/images/product/surgical-tool.jpg',
        }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"{product.name} added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

def view_cart(request):
    context = get_common_context(request)
    return render(request, 'products/cart.html', context)

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))
