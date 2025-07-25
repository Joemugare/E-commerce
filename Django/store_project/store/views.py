from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from .models import Product, Price

# Stripe API key setup
stripe.api_key = settings.STRIPE_SECRET_KEY

class HomeView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['cart'] = self.request.session.get('cart', {})
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLIC_KEY  # Add for Stripe.js
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

class CreateCheckoutView(View):
    @csrf_exempt  # Required for POST with CSRF token in AJAX
    def post(self, request, *args, **kwargs):
        price = get_object_or_404(Price, pk=kwargs["pk"])  # Use Price model directly
        product = price.product  # Assuming Price has a ForeignKey to Product
        payment_method = request.POST.get('payment_method')

        try:
            if payment_method == 'stripe':
                # Create Stripe Checkout Session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'kes',
                            'product_data': {
                                'name': product.name,
                            },
                            'unit_amount': int(price.price * 100),  # Convert to cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),
                )
                return JsonResponse({'redirect_url': checkout_session.url})
            elif payment_method == 'mpesa':
                # Placeholder for M-Pesa logic (e.g., initiate STK Push)
                # Replace with your M-Pesa API integration
                phone_number = request.POST.get('phone_number')
                if not phone_number:
                    return JsonResponse({'error': 'Phone number is required for M-Pesa'}, status=400)
                # Example: Call M-Pesa API to initiate STK Push
                # mpesa_response = initiate_mpesa_stk_push(phone_number, price.price)
                return JsonResponse({'message': 'STK Push sent to your phone'})
            else:
                return JsonResponse({'error': 'Invalid payment method'}, status=400)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

class SuccessView(TemplateView):
    template_name = 'store/success.html'

class CancelView(TemplateView):
    template_name = 'store/cancel.html'

class AboutView(TemplateView):
    template_name = 'store/about.html'

class ContactView(TemplateView):
    template_name = 'store/contact.html'

class MpesaCallbackView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Add M-Pesa callback logic here
        return JsonResponse({"status": "received"})

class StripeWebhookView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Update order status or perform other actions
            # Example: Order.objects.filter(stripe_session_id=session.id).update(status='completed')
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'event not handled'})

class AddToCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        cart[str(pk)] = cart.get(str(pk), 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'message': 'Added to cart'})

class RemoveFromCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        if str(pk) in cart:
            cart[str(pk)] -= 1
            if cart[str(pk)] <= 0:
                del cart[str(pk)]
        request.session['cart'] = cart
        return JsonResponse({'message': 'Removed from cart'})