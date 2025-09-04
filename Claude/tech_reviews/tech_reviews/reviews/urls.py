from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review_list'),                  # List of reviews
    path('<int:id>/', views.review_detail, name='review_detail'),    # Review detail
    path('create/', views.create_review, name='create_review'),      # Create review
    path('about/', views.about, name='about'),                       # About page
]