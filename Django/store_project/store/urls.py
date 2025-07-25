from django.urls import path
from .views import (
    HomeView, ProductListView, CreateCheckoutView,
    SuccessView, CancelView, AboutView, ContactView,
    MpesaCallbackView, StripeWebhookView, AddToCartView, RemoveFromCartView,
    ProductDetailView  # ← add this import
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # ← this line fixes the issue
    path('checkout/<int:pk>/', CreateCheckoutView.as_view(), name='create_checkout'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('mpesa/callback/', MpesaCallbackView.as_view(), name='mpesa_callback'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]
