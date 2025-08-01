from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/<int:pk>/', views.brand_detail, name='brand_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
]
