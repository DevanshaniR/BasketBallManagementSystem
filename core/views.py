from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime


@api_view(['GET'])
def health(request):
    return JsonResponse({'success': True, 'status': "live", "timestamp": datetime.utcnow()})
