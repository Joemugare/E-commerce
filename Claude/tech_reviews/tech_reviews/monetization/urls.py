from django.urls import path
from . import views

app_name = "monetization"

urlpatterns = [
    path('ad_dashboard/', views.ad_dashboard, name='ad_dashboard'),
    path('affiliate/', views.affiliate_products, name='affiliate_products'),
    path('premium/', views.premium_content_list, name='premium_content'),
    path('premium/<int:content_id>/', views.purchase_premium_content, name='purchase_premium'),
]
