from django.urls import path
from . import views

urlpatterns = [
    path('user/getall', views.getUsers),
    path('user/getOne/<str:pk>', views.getUser),
    path('user/create', views.createUser),
    path('user/update/<str:pk>', views.updateUser),
    path('user/delete/<str:pk>', views.deleteUser),
]