import uuid
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
        print('mapbox matching error')
        road.delete()
        return
    print('{}, {}'.format(city, state))

    image_path = rating_data['image']
    try:
        rate = cracker(image_path)
        print(rate)
        point_rate = int(rate)
        if point_rate < 1 or point_rate > 10:
            raise RatingError
    except:
        print('rating error')
        road.delete()
        return

    print("image path:{}, rate:{}".format(image_path, point_rate))
    if rating_data['previous_id'] == uuid.UUID('00000000-0000-0000-0000-000000000000').hex:
        previous_rate = point_rate
    else:
        try:
            previous_road = Road.objects.get(pk=rating_data['previous_id'])
            if previous_road.point_rate is not None:
                previous_rate = int(previous_road.point_rate)
            else:
                previous_rate = point_rate
        except Road.DoesNotExist:
            previous_rate = point_rate

    line_rate = point_rate
    if previous_rate != 0:
        line_rate = (previous_rate + point_rate) / 2

    road.point_rate = point_rate
    road.line_rate = line_rate
    road.city = city
    road.state = state
    road.street = street
    road.save()



