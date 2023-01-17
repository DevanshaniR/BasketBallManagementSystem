from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Sum, Count
from django.db.models import ExpressionWrapper, F, fields
from rest_framework.response import Response

from core.models import Game, Coach, UserRole, TeamStat, Player, PlayerStat, Team, UserLoginDetails
from core.serializers import GameSerializer, PlayerSerializer, TeamSerializer


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


@api_view(['GET'])
def player_score(request, user_id):
    try:
        user_role = UserRole.objects.get(user_id=user_id)
        if user_role.role.type == 'P':
            return JsonResponse({'success': False, "error": "not Authorized to access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        filter_score = request.query_params.get('filter_score')
        coach_rec = Coach.objects.get(user_id=user_id)
        team_id = coach_rec.team_id
        players = Player.objects.filter(team_id=team_id)
        team_name = players[0].team.name
        serializer = PlayerSerializer(players, many=True)
        player_data = serializer.data
        new_player_array = []
        for pl in player_data:
            player_id = pl['id']
            av_score_obj = PlayerStat.objects.filter(player_id=player_id).aggregate(Avg('score'))
            av_score = av_score_obj['score__avg']
            if filter_score is None:
                player_obj = {'id': player_id, 'name': pl['name'], 'height': pl['height'],
                              'average_score': av_score if av_score is not None else 0,
                              'games_participated': len(PlayerStat.objects.filter(player_id=player_id))}
                new_player_array.append(player_obj)
            else:

                if av_score is not None and float(av_score) >= float(filter_score):
                    player_obj = {'id': player_id, 'name': pl['name'], 'height': pl['height'],
                                  'average_score': av_score_obj['score__avg'],
                                  'games_participated': len(PlayerStat.objects.filter(player_id=player_id))}
                    new_player_array.append(player_obj)

        return JsonResponse(
            {'success': True, 'team_name': team_name, 'average_score': av_score_obj, 'player_data': new_player_array})
    except Coach.DoesNotExist:
        return JsonResponse({'success': False, "error": "user not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_team_details(request, user_id):
    try:
        user_role = UserRole.objects.get(user_id=user_id)
        if user_role.role.type != 'A':
            return JsonResponse({'success': False, "error": "not Authorized to access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        team_data = serializer.data
        for item in team_data:
            average_score = TeamStat.objects.filter(team_id=item['id']).aggregate(Avg('score'))
            item['average_score'] = average_score
            players = Player.objects.filter(team_id=item['id'])
            serializer = PlayerSerializer(players, many=True)
            player_data = serializer.data
            for pl in player_data:
                player_id = pl['id']
                av_score_obj = PlayerStat.objects.filter(player_id=player_id).aggregate(Avg('score'))
                pl['average_score'] = av_score_obj
                pl['games_participated'] = len(PlayerStat.objects.filter(player_id=player_id))
            item['player_data'] = player_data
        return JsonResponse({'success': True, 'teams': team_data})
    except Team.DoesNotExist:
        return JsonResponse({'success': False, "error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def login_details(request, user_id):
    try:
        user_role = UserRole.objects.get(user_id=user_id)
        if user_role.role.type != 'A':
            return JsonResponse({'success': False, "error": "not Authorized to access"},
                                status=status.HTTP_401_UNAUTHORIZED)

        duration = ExpressionWrapper(F('logout_time') - F('login_time'), output_field=fields.DurationField())
        login_data = UserLoginDetails.objects.values('user_id').annotate(duration=Sum(duration)).annotate(
            login_count=Count('user_id')).order_by('user_id')

        return Response({
            'success': True,
            'stats': login_data,
            'total_online': UserRole.objects.filter(is_logged_in=True).aggregate(Count('id')),
            'online_users': UserRole.objects.filter(is_logged_in=True).values_list('user_id', flat=True),
        })
    except Exception as error:
        return JsonResponse({'success': False, "error": error}, status=status.HTTP_404_NOT_FOUND)
