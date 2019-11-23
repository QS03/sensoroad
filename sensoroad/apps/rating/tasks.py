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
            city = context[1]['text']
            state = context[2]['text']
        except IndexError:
            raise MapboxError
    except MapboxError:
        road.delete()
        return

    image_path = rating_data['image']
    print("image path:{}".format(image_path))
    try:
        rate = cracker(image_path)
        point_rate = int(rate)
        if point_rate < 1 or point_rate > 10:
            raise RatingError
    except RatingError:
        road.delete()
        return
    except:
        road.delete()
        return

    try:
        previous_road = Road.objects.get(pk=rating_data['previous_id'])
        if previous_road.point_rate is not None:
            previous_rate = int(previous_road.point_rate)
        else:
            previous_rate = 0
    except Road.DoesNotExist:
        previous_rate = 0

    line_rate = point_rate
    if previous_rate != 0:
        line_rate = (previous_rate + point_rate) / 2

    road.point_rate = point_rate
    road.line_rate = line_rate
    road.city = city
    road.state = state
    road.street = street
    road.save()



