from django.urls import path
from . import views

urlpatterns = [
    path('opendota/getOpendotaHeroes/', views.opendotaGetHeroes),
    path('getParsedHeroes/', views.getParsedHeroes),
    path('saveHeroes/', views.saveHeroes),
    path('getHeroes/', views.getHeroes),
    path('getHero/<str:id>/', views.getHero),
]