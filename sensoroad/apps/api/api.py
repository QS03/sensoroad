import sys
import uuid

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from sensoroad.apps.road.models import Road

@csrf_exempt
@require_POST
@login_required()
def upload_image(request):
    body = request.POST
    road = Road()
    road.id = uuid.UUID(body['id']).hex
    road.image = request.FILES['image']
    road.longitude = float(body['longitude'])
    road.latitude = float(body['latitude'])
    road.user_id = request.user.id

    print(road)
    return JsonResponse(dict(
        success=True, message="image uploaded successfully"))
