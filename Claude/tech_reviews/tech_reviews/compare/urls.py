# compare/urls.py
from django.urls import path
from . import views

app_name = 'compare'
urlpatterns = [
    path('compare/', views.compare_products, name='compare_list'),
    path('add/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('remove/<int:product_id>/', views.remove_from_compare, name='remove_from_compare'),
]