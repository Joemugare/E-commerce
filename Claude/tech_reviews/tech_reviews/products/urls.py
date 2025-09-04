from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),  # Changed id to pk
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
]