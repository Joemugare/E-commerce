# tech_reviews/urls.py (Main project URLs)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # This should only import home and newsletter views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Home page
    path('', views.home, name='home'),
    # App URLs
    path('users/', include('users.urls', namespace='users')),
    path('compare/', include('compare.urls', namespace='compare')),
    path('deals/', include('deals.urls', namespace='deals')),
    path('products/', include('products.urls', namespace='products')),
    path('about/', include('about.urls', namespace='about')),
    path('monetization/', include('monetization.urls', namespace='monetization')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    # Newsletter subscription
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path("categories/", include("categories.urls", namespace="categories")),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)