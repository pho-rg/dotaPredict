from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Match
from .service import fetch_steam_live_league_games, get_parsed_live_matches, transformMatchData, updateLiveMatches, get_parsed_win_history, updateWinnerMatches

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def steamGetLiveLeagueGames(request):
    try:
        data = fetch_steam_live_league_games()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getParsedLiveMatches(request):
    try:
        parsed_matches = get_parsed_live_matches()
        return JsonResponse(parsed_matches, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def saveLiveMatches(request):
    result = updateLiveMatches()

    if result["success"]:
        return JsonResponse({
            "created": result["created"],
            "updated": result["updated"],
            "total": result["total"]
        })
    else:
        return JsonResponse({'error': result["error"]}, status=500)

@api_view(['GET'])
def getMatches(request):
    try:
        matches = Match.objects.all().values()
        transformed_matches = [transformMatchData(match) for match in matches]
        return JsonResponse(transformed_matches, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getAllLiveMatches(request):
    try:
        matches = Match.objects.exclude(match_status="match_ended").values()
        transformed_matches = [transformMatchData(match) for match in matches]
        return JsonResponse(transformed_matches, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getMatch(request, id):
    try:
        match = Match.objects.filter(match_id=id).values().first()
        if not match:
            return JsonResponse({'error': f'Match with id {id} not found'}, status=404)
        return JsonResponse(transformMatchData(match), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getInDraftMatches(request):
    try:
        matches = Match.objects.filter(draft_in_progress=True).values()
        transformed_matches = [transformMatchData(match) for match in matches]
        return JsonResponse(transformed_matches, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getMatchesWinner(request):
    try:
        matches_winner = get_parsed_win_history()
        return JsonResponse(matches_winner, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def getAllMatchesHistory(request):
    try:
        matches = Match.objects.exclude(radiant_win=-1).values()
        transformed_matches = [transformMatchData(match) for match in matches]

        return JsonResponse(transformed_matches, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def saveWinnerHistory(request):
    result = updateWinnerMatches()

    if result["success"]:
        return JsonResponse({
            "updated": result["updated"],
            "not_found": result["not_found"],
            "total": result["total"]
        })
    else:
        return JsonResponse({'error': result["error"]}, status=500)