from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Hero
from .service import fetch_opendota_heroes, get_parsed_heroes


@api_view(['GET'])
def opendotaGetHeroes(request):
    try:
        data = fetch_opendota_heroes()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getParsedHeroes(request):
    try:
        parsed_heroes = get_parsed_heroes()
        return JsonResponse(parsed_heroes, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def saveHeroes(request):
    try:
        parsed_heroes = get_parsed_heroes()
        created_count = 0
        updated_count = 0
        for hero_data in parsed_heroes:
            obj, created = Hero.objects.update_or_create(
                hero_id=hero_data["hero_id"],
                defaults={
                    "hero_id": hero_data["hero_id"],
                    "name": hero_data["name"]
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        return JsonResponse({
            "created": created_count,
            "updated": updated_count,
            "total": len(parsed_heroes)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getHeroes(request):
    try:
        heroes = Hero.objects.all().values()
        return JsonResponse(list(heroes), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def getHero(request, id):
    try:
        hero = Hero.objects.filter(hero_id=id).values().first()
        if not hero:
            return JsonResponse({'error': f'Hero with id {id} not found'}, status=404)
        return JsonResponse(hero, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)