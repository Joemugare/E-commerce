from django.shortcuts import render, get_object_or_404
from .models import Deal

def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'deals/deal_list.html', {'deals': deals})

def deal_detail(request, id):
    deal = get_object_or_404(Deal, id=id)
    return render(request, 'deals/deal_detail.html', {'deal': deal})
