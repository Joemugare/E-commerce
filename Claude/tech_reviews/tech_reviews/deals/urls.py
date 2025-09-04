from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.deal_list, name='deal_list'),          # <-- added
    path('<int:id>/', views.deal_detail, name='deal_detail'),
]
