# matchapp/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('steam/GetLiveLeagueGames', views.SteamGetLiveLeagueGames),
    #path('getMatches/<str:pk>/', views.getMatches),
    #path('getMatch/<str:pk>/', views.getMatch),
    #path('getMatchesInDraft/', views.getInDraftMatches),
    #path('isMatchInDraft/<str:pk>/', views.isMatchInDraft),
]