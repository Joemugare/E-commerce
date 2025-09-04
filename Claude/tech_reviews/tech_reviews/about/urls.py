from django.urls import path
from . import views

app_name = 'about'  # <- important for namespacing

urlpatterns = [
    path('', views.about_view, name='about'),  # <- this 'about' is the view name
]
