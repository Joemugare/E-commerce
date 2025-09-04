# compare/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from products.models import Product

def compare_products(request):
    product_ids = request.session.get('compare_products', [])
    products = Product.objects.filter(id__in=product_ids)[:4]
    context = {'products': products}
    return render(request, 'compare/compare_products.html', context)

def add_to_compare(request, product_id):
    if 'compare_products' not in request.session:
        request.session['compare_products'] = []
    if product_id not in request.session['compare_products'] and len(request.session['compare_products']) < 4:
        request.session['compare_products'].append(product_id)
        request.session.modified = True
    return redirect('compare:compare_list')  # Redirect to comparison page for testing

def remove_from_compare(request, product_id):
    if 'compare_products' in request.session and product_id in request.session['compare_products']:
        request.session['compare_products'].remove(product_id)
        request.session.modified = True
    return redirect('compare:compare_list')