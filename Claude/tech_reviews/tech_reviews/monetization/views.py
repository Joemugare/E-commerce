# monetization/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def ad_dashboard(request):
    return render(request, 'monetization/ad_dashboard.html')

@login_required
def affiliate_products(request):
    return render(request, 'monetization/affiliate_products.html')

@login_required
def premium_content_list(request):
    return render(request, 'monetization/premium_content.html')

@login_required
def purchase_premium_content(request, content_id):
    return render(request, 'monetization/purchase_premium.html')
