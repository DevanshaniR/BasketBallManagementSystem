from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime

from core.models import Game
from core.serializers import GameSerializer


@api_view(['GET'])
def health(request):
    return JsonResponse({'success': True, 'status': "live", "timestamp": datetime.utcnow()})


@api_view(['GET'])
def score_board(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return JsonResponse({'success': True, 'score_board': serializer.data})
