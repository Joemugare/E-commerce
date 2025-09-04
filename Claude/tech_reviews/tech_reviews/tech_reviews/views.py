# tech_reviews/views.py (Main project views)
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # Your home view logic
    context = {
        'total_reviews': 100,  # Replace with actual count
        'trending_reviews': [],  # Replace with actual data
        'products': [],  # Replace with actual data
    }
    return render(request, 'home.html', context)

def newsletter_subscribe(request):
    if request.method == 'POST':
        # Handle newsletter subscription
        return HttpResponse('Subscribed successfully!')
    return HttpResponse('Invalid request')