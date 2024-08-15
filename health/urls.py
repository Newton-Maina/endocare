# health/urls.py
from django.urls import path
from .views import health_profile_view

urlpatterns = [
    path('profile/', health_profile_view, name='health_profile'),
]
