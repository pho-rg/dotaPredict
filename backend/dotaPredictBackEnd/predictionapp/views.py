from django.http import JsonResponse
from django.shortcuts import render
from .service import get_ai_models_list, predict_match
from rest_framework.decorators import api_view

@api_view(['GET'])
def getAvailableModels(request):
    return JsonResponse(get_ai_models_list(), safe=False)

@api_view(['POST'])
def predictMatch(request):
    try:
        # extract data from the body
        data = request.data
        hero_picks = data.get('hero_picks', [])
        all_models = get_ai_models_list()

        # find AI model, default if not specified
        default_model = next((x for x in all_models if x.get('default')), None)
        ai_model_id = data.get('ai_model_id', default_model['id'] if default_model else None)

        # call prediction service
        prediction = predict_match(hero_picks, int(ai_model_id))
        return JsonResponse(prediction, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
