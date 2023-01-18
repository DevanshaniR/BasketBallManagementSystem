from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime
from rest_framework.permissions import AllowAny

from core.service import BasketBallService


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return JsonResponse({'success': True, 'status': "live", "timestamp": datetime.utcnow()})


# view the scoreboard which display all games and final scores
@api_view(['GET'])
@login_required
def score_board(request):
    basketball_service = BasketBallService()
    return basketball_service.get_scoreboard()


# coach can view his team to view list of players,average score of the team,player personal details
@api_view(['GET'])
@login_required
def coach(request, user_id):
    basketball_service = BasketBallService()
    return basketball_service.get_coach_details(user_id)


# coach can filter players based on average score
# filter_score pass as a query parameter so >90 percentile average score also can filter
@api_view(['GET'])
@login_required
def player_score(request, user_id):
    basketball_service = BasketBallService()
    return basketball_service.get_player_score(request, user_id)


# admin can view all team details,average scores,players list & details
@api_view(['GET'])
@login_required
def all_team_details(request, user_id):
    basketball_service = BasketBallService()
    return basketball_service.get_all_team_details(user_id)


# view statistics of site usage
@api_view(['GET'])
@login_required
def login_details(request, user_id):
    basketball_service = BasketBallService()
    return basketball_service.view_login_statistics(user_id)
