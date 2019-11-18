import sys
import uuid
from datetime import datetime
from http import HTTPStatus

from django.db import IntegrityError
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from sensoroad.apps.road.models import Road
from sensoroad.apps.user.models import User


@csrf_exempt
@require_POST
@login_required()
def upload_image(request):
    body = request.POST
    road = Road()
    road.id = uuid.UUID(body['id']).hex
    road.previous_id = uuid.UUID(body['previous_id']).hex
    road.image = request.FILES['image']
    road.longitude = float(body['longitude'])
    road.latitude = float(body['latitude'])
    road.taken_at = datetime.strptime(body['taken_at'], "%Y-%m-%dT%H:%M:%S")
    road.user = User.objects.get(pk=body['device_id'])

    try:
        road.save()
        status = 'success'
        obj = Road.objects.get(pk=road.id)
        message = obj.get_object_for_mobile()
        code = HTTPStatus.OK
    except IntegrityError:
        obj = Road.objects.get(pk=road.id)
        status = 'conflict'
        message = obj.get_object_for_mobile()
        code = HTTPStatus.CONFLICT
    except:
        status = 'failed'
        message = 'unknown error'
        code = HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        print(message)
        return JsonResponse({'status': status, 'message': message}, status=code)

