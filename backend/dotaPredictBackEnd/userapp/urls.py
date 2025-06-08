from django.urls import path
from . import views

urlpatterns = [
    path('getall/', views.getUsers),
    path('getOne/<str:pk>/', views.getUser),
    path('create/', views.createUser),
    path('update/<str:pk>/', views.updateUser),
    path('delete/<str:pk>/', views.deleteUser),
    path('login/', views.login),
    path('register/', views.register),
]