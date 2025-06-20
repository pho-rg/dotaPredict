# predictionapp/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('getAvailableModels/', views.getAvailableModels),
    path('predictMatch/', views.predictMatch),
]