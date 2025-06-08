from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Match
from .service import fetch_steam_live_league_games, get_parsed_live_matches

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
    try:
        parsed_matches = get_parsed_live_matches()
        created_count = 0
        updated_count = 0
        for match_data in parsed_matches:
            obj, created = Match.objects.update_or_create(
                match_id=match_data["match_id"],
                defaults={
                    "radiant_team": match_data["radiant_team"],
                    "dire_team": match_data["dire_team"],
                    "draft_in_progress": match_data["draft_in_progress"],
                    "radiant_win_chance": match_data["radiant_win_chance"],

                    "radiant_pick1": match_data["radiant_pick1"],
                    "radiant_pick2": match_data["radiant_pick2"],
                    "radiant_pick3": match_data["radiant_pick3"],
                    "radiant_pick4": match_data["radiant_pick4"],
                    "radiant_pick5": match_data["radiant_pick5"],

                    "dire_pick1": match_data["dire_pick1"],
                    "dire_pick2": match_data["dire_pick2"],
                    "dire_pick3": match_data["dire_pick3"],
                    "dire_pick4": match_data["dire_pick4"],
                    "dire_pick5": match_data["dire_pick5"],

                    "radiant_ban1": match_data["radiant_ban1"],
                    "radiant_ban2": match_data["radiant_ban2"],
                    "radiant_ban3": match_data["radiant_ban3"],
                    "radiant_ban4": match_data["radiant_ban4"],
                    "radiant_ban5": match_data["radiant_ban5"],
                    "radiant_ban6": match_data["radiant_ban6"],
                    "radiant_ban7": match_data["radiant_ban7"],

                    "dire_ban1": match_data["dire_ban1"],
                    "dire_ban2": match_data["dire_ban2"],
                    "dire_ban3": match_data["dire_ban3"],
                    "dire_ban4": match_data["dire_ban4"],
                    "dire_ban5": match_data["dire_ban5"],
                    "dire_ban6": match_data["dire_ban6"],
                    "dire_ban7": match_data["dire_ban7"],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        return JsonResponse({
            "created": created_count,
            "updated": updated_count,
            "total": len(parsed_matches)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getMatches(request):
    try:
        matches = Match.objects.all().values()
        return JsonResponse(list(matches), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getMatch(request, id):
    try:
        match = Match.objects.filter(match_id=id).values().first()
        if not match:
            return JsonResponse({'error': f'Match with id {id} not found'}, status=404)
        return JsonResponse(match, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getInDraftMatches(request):
    try:
        matches = Match.objects.filter(draft_in_progress=True).values()
        return JsonResponse(list(matches), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)