# matchapp/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('steam/getLiveLeagueGames/', views.steamGetLiveLeagueGames),
    path('getParsedLiveMatches/', views.getParsedLiveMatches),
    path('saveLiveMatches/', views.saveLiveMatches),
    path('getAll/', views.getMatches),
    path('getAllLive/', views.getAllLiveMatches),
    path('getOne/<str:id>/', views.getMatch),
    path('getMatchesInDraft/', views.getInDraftMatches),
    path('getMatchesWinner/', views.getMatchesWinner),
    path('saveWinnerHistory/', views.saveWinnerHistory),
    path('getAllMatchesHistory/', views.getAllMatchesHistory),
]