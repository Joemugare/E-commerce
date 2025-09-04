from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Review
from products.models import Product
from products.forms import ReviewForm

def review_list(request):
    """
    List all reviews with optional filters: video type, search query, category, sort.
    """
    reviews = Review.objects.select_related('product', 'user').all()

    # Filters
    if request.GET.get('type') == 'video':
        reviews = reviews.filter(video_url__isnull=False)
    if request.GET.get('q'):
        reviews = reviews.filter(title__icontains=request.GET.get('q'))
    if request.GET.get('category'):
        reviews = reviews.filter(product__category__name__iexact=request.GET.get('category'))
    
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'newest':
        reviews = reviews.order_by('-created_at')
    elif sort == 'oldest':
        reviews = reviews.order_by('created_at')
    elif sort == 'rating':
        reviews = reviews.order_by('-rating')
    elif sort == 'name':
        reviews = reviews.order_by('title')

    # Pagination
    paginator = Paginator(reviews, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, id):
    """
    Show single review detail.
    """
    review = get_object_or_404(Review, id=id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def home(request):
    """
    Home page with trending reviews and featured video reviews.
    """
    trending_reviews = Review.objects.order_by('-created_at')[:6]
    featured_video_reviews = Review.objects.filter(video_url__isnull=False).order_by('-created_at')[:3]
    products = Product.objects.all()

    context = {
        'trending_reviews': trending_reviews,
        'featured_video_reviews': featured_video_reviews,
        'products': products,
        'total_reviews': Review.objects.count(),
    }
    return render(request, 'home.html', context)


@login_required
def create_review(request):
    """
    Handle review submission from the product detail modal.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
        # Redirect back to the product detail page
        return redirect('products:product_detail', id=product.id)
    # If someone tries to access this URL via GET, redirect to products list
    return redirect('products:product_list')


def about(request):
    """
    Placeholder about page.
    """
    return render(request, 'reviews/about.html', {'message': 'About page not yet implemented'})
