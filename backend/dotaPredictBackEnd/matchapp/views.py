import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

@require_GET
def SteamGetLiveLeagueGames(request):
    api_key = getattr(settings, 'STEAM_API_KEY', None)

    if not api_key:
        return JsonResponse({'error': 'STEAM_API_KEY is not configured in settings.'}, status=500)

    api_url = f"https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key={api_key}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Will raise exception for 4XX or 5XX responses
        data = response.json()
        return JsonResponse(data, safe=False, status=200)
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch data from Steam API', 'details': str(e)}, status=500)