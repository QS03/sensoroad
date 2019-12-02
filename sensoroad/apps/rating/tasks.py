import uuid
import json
import requests
from celery import shared_task
from sensoroad.apps.rating.cracker import cracker
from django.conf import settings

from mapbox import Geocoder

from sensoroad.apps.road.models import Road


class MapboxError(Exception):
    pass


class RatingError(Exception):
    pass


@shared_task
def task_rating_georeverse(rating_data):
    road = Road.objects.get(pk=rating_data['id'])

    longitude = rating_data['longitude']
    latitude = rating_data['latitude']
    geocoder = Geocoder(access_token=settings.MAPBOX_ACCESS_TOKEN)
    response = geocoder.reverse(lon=longitude, lat=latitude)

    try:
        if response.status_code != 200:
            raise MapboxError
        geo_data = response.geojson()['features']
        if len(geo_data) == 0:
            raise MapboxError
        try:
            street = geo_data[0]['text']
            context = geo_data[0]['context']
            for item in context:
                if 'place.' in item['id']:
                    city = item['text']
                if 'region.' in item['id']:
                    state = item['text']

            if city is None or state is None:
                raise MapboxError
        except IndexError:
            raise MapboxError
    except MapboxError:
        street = None
        city = None
        state = None

    print('{}, {}'.format(city, state))

    image_path = rating_data['image']
    try:
        rate = cracker(image_path)
        point_rate = int(rate)
        if point_rate < 1:
            point_rate = 1

        if point_rate > 10:
            point_rate = 10
    except:
        point_rate = None

    print("image path:{}, rate:{}".format(image_path, point_rate))

    road.point_rate = point_rate
    road.city = city
    road.state = state
    road.street = street

    url_prefix = 'https://api.mapbox.com/matching/v5/mapbox/driving'
    params = {
        'geometries': 'geojson',
        'radiuses': '25;25',
        'steps': 'true',
        'access_token': settings.MAPBOX_ACCESS_TOKEN
    }

    try:
        prev_road = Road.objects.get(pk=uuid.UUID(rating_data['previous_id']).hex)
        prev_longitude = prev_road.longitude
        prev_latitude = prev_road.latitude
        prev_point_rate = prev_road.point_rate

        road.prev_latitude = prev_latitude
        road.prev_longitude = prev_longitude
        if point_rate is not None and prev_point_rate is not None:
            road.line_rate = int((int(point_rate) + int(prev_point_rate)) / 2)
        elif point_rate is not None:
            road.line_rate = point_rate
        elif prev_point_rate is not None:
            road.line_rate = prev_point_rate

        coordinates = "{},{};{},{}".format(prev_longitude, prev_latitude, longitude, latitude)
        url = '{}/{}'.format(url_prefix, coordinates)

        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'Ok':
                road.matching = json.dumps(data['matchings'][0]['geometry'])
            else:
                road.matching = json.dumps({'coordinates': [
                    [longitude, latitude],
                    [prev_longitude, prev_latitude]],
                    'type': 'LineString'
                })
        else:
            road.matching = json.dumps({'coordinates': [
                [longitude, latitude],
                [prev_longitude, prev_latitude]],
                'type': 'LineString'
            })
    except Road.DoesNotExist:
        road.prev_latitude = longitude
        road.prev_longitude = latitude
        road.matching = json.dumps({'coordinates': [
            [longitude, latitude],
            [longitude, latitude]],
            'type': 'LineString'
        })

    road.save()



