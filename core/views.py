from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Sum, Count

from core.models import Game, Coach, UserRole, TeamStat, Player, PlayerStat
from core.serializers import GameSerializer, PlayerSerializer


@api_view(['GET'])
def health(request):
    return JsonResponse({'success': True, 'status': "live", "timestamp": datetime.utcnow()})


@api_view(['GET'])
def score_board(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return JsonResponse({'success': True, 'score_board': serializer.data})


@api_view(['GET'])
def coach(request, user_id):
    try:
        user_role = UserRole.objects.get(user_id=user_id)
        if user_role.role.type == 'P':
            return JsonResponse({'success': False, "error": "not Authorized to access"},
                                status=status.HTTP_401_UNAUTHORIZED)

        coach_rec = Coach.objects.get(user_id=user_id)
        team_id = coach_rec.team_id
        average_score = TeamStat.objects.filter(team_id=team_id).aggregate(Avg('score'))
        players = Player.objects.filter(team_id=team_id)
        team_name = players[0].team.name
        serializer = PlayerSerializer(players, many=True)
        player_data = serializer.data
        new_player_array = []
        for pl in player_data:
            player_id = pl['id']
            av_score_obj = PlayerStat.objects.filter(player_id=player_id).aggregate(Avg('score'))
            av_score = av_score_obj['score__avg']

            player_obj = {'id': player_id, 'name': pl['name'], 'height': pl['height'],
                          'average_score': av_score if av_score is not None else 0,
                          'games_participated': len(PlayerStat.objects.filter(player_id=player_id))}
            new_player_array.append(player_obj)

        return JsonResponse(
            {'success': True, 'team_name': team_name, 'average_score': average_score, 'player_data': new_player_array})
    except Coach.DoesNotExist:
        return JsonResponse({'success': False, "error": "user not found"}, status=status.HTTP_404_NOT_FOUND)
