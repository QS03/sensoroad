import sys
import uuid
from datetime import datetime
from http import HTTPStatus

import iso8601
from django.db import IntegrityError
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings

from sensoroad.apps.road.models import Road
from sensoroad.apps.user.models import User
from sensoroad.apps.rating.tasks import task_rating_georeverse


@csrf_exempt
@require_POST
def upload_image(request):
    if not request.user.is_authenticated:
        status = 'failed'
        message = 'Unauthorized'
        code = HTTPStatus.UNAUTHORIZED  # 401
        return JsonResponse(
            {
                'meta': {'status': status},
                'message': message
            },
            status=code,
        )

    try:
        body = request.POST
        road = Road()
        road.id = uuid.UUID(body['id']).hex
        road.previous_id = uuid.UUID(body['previous_id']).hex
        road.image = request.FILES['image']
        road.longitude = float(body['longitude'])
        road.latitude = float(body['latitude'])
        road.taken_at = iso8601.parse_date(body['taken_at'])
        road.user = User.objects.get(pk=request.user.id)
    except ValueError:
        status = 'failed'
        message = 'Invalid key-value pair'
        code = HTTPStatus.UNPROCESSABLE_ENTITY  # 422
        return JsonResponse(
            {
                'meta': {'status': status},
                'message': message
            },
            status=code,
        )
    except MultiValueDictKeyError:
        status = 'failed'
        message = 'Missing required key-value pair'
        code = HTTPStatus.BAD_REQUEST  # 400
        return JsonResponse(
            {
                'meta': {'status': status},
                'message': message
            },
            status=code,
        )

    try:
        road.save()
        status = 'success'
        obj = Road.objects.get(pk=road.id)
        message = obj.get_object_for_mobile()
        code = HTTPStatus.OK
        task_rating_georeverse.delay(road.get_object_for_rating())

        return JsonResponse(
            {
                'meta': {'status': status},
                'data': message,
            },
            status=code,
        )
    except IntegrityError:
        obj = Road.objects.get(pk=road.id)
        status = 'conflict'
        message = obj.get_object_for_mobile()
        code = HTTPStatus.CONFLICT  # 409
    except:
        status = 'failed'
        message = 'unknown error'
        code = HTTPStatus.INTERNAL_SERVER_ERROR  # 500

    return JsonResponse(
        {
            'meta': {'status': status},
            'message': message,
        },
        status=code,
    )

