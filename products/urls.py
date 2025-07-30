from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('index/', views.index, name='index'),  # Optional home/index route
    path('', views.product_list, name='product_list'),  # List all products
    path('<int:pk>/', views.product_detail, name='product_detail'),  # Single product

    path('brands/', views.brand_list, name='brand_list'),  # List all brands
    path('brands/<int:pk>/', views.brand_detail, name='brand_detail'),  # Brand detail

    path('categories/', views.category_list, name='category_list'),  # Category list
]
