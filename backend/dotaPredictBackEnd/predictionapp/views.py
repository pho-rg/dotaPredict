from django.http import JsonResponse
from .service import get_ai_models_list, predict_match, get_default_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from userapp.permissions import IsAnalyst

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAnalyst])
def getAvailableModels(request):
    return JsonResponse(get_ai_models_list(), safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAnalyst])
def predictMatch(request):
    try:
        # extract data from the body
        data = request.data
        hero_picks = data.get('hero_picks', [])

        # find AI model, default if not specified
        default_model = get_default_model()
        ai_model_id = data.get('ai_model_id', default_model['id'] if default_model else None)

        # call prediction service
        prediction = predict_match(hero_picks, int(ai_model_id))
        return JsonResponse(prediction, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
