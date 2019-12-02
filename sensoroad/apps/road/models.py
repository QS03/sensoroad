import uuid
import json
import requests
from django.db import models
from django.conf import settings
# Create your models here.


class Road(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    previous_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', blank=False)
    taken_at = models.DateTimeField(blank=True, null=True)

    longitude = models.FloatField(blank=False)
    latitude = models.FloatField(blank=False)
    point_rate = models.IntegerField(blank=True, null=True)

    prev_longitude = models.FloatField(blank=True, null=True)
    prev_latitude = models.FloatField(blank=True, null=True)
    line_rate = models.IntegerField(blank=True, null=True)
    matching = models.TextField(blank=True, null=True)

    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'road'

    def __str__(self):
        return "{}".format(self.id)

    def get_object_for_mobile(self):
        image_path = settings.MEDIA_URL + self.image.path.split(settings.MEDIA_URL)[1]
        json = {
            'id': self.id,
            'previous_id': self.previous_id,
            'image': image_path,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'taken_at': self.taken_at
        }
        return json

    def get_object_for_dashboard(self):
        image_path = settings.MEDIA_URL + self.image.path.split(settings.MEDIA_URL)[1]

        if self.point_rate is None:
            point_rate = 1
        else:
            point_rate = int(self.point_rate)

        if self.line_rate is None:
            line_rate = 1
        else:
            line_rate = int(self.line_rate)

        point_data = {
             'coordinate': [self.longitude, self.latitude],
             'rate': point_rate,
             'image_url': image_path
         }

        line_data = {
            'coordinates': [
                [self.longitude, self.latitude],
                [self.prev_longitude, self.prev_latitude],
            ],
            'rate': line_rate,
            'matching': self.matching,
        }

        return {
            'point_data': point_data,
            'line_data': line_data
        }

    def get_object_for_rating(self):
        data = {
            'id': self.id,
            'previous_id': self.previous_id,
            'image': self.image.path,
            'longitude': self.longitude,
            'latitude': self.latitude,
        }
        return data

    @staticmethod
    def get_all_objects():
        roads = Road.objects.all()
        road_data = []
        for road in roads:
            road_data.append({
                    'id': road.id,
                    'previous_id': road.previous_id,
                    'image': road.image.path,
                    'latitude': road.latitude,
                    'longitude': road.longitude,
                    'point_rate': road.point_rate,
                    'line_rate': road.line_rate,
                    'matching': road.matching,
                    'city': road.city,
                    'state': road.state
                }
            )

        return road_data

    @staticmethod
    def fill_matching_data():
        roads = Road.objects.all()

        url_prefix = 'https://api.mapbox.com/matching/v5/mapbox/driving'
        params = {
            'geometries': 'geojson',
            'radiuses': '25;25',
            'steps': 'true',
            'access_token': settings.MAPBOX_ACCESS_TOKEN
            }

        for road in roads:
            longitude = road.longitude
            latitude = road.latitude
            point_rate = road.point_rate

            try:
                prev_road = Road.objects.get(pk=road.previous_id)
                prev_longitude = prev_road.longitude
                prev_latitude = prev_road.latitude
                prev_point_rate = prev_road.point_rate

                road.prev_latitude = prev_latitude
                road.prev_longitude = prev_longitude
                if point_rate is not None and prev_point_rate is not None:
                    road.line_rate = int((int(point_rate) + int(prev_point_rate))/2)
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
                            [prev_longitude, prev_latitude]]
                        })
                else:
                    road.matching = json.dumps({'coordinates': [
                        [longitude, latitude],
                        [prev_longitude, prev_latitude]]
                    })
            except Road.DoesNotExist:
                road.prev_latitude = longitude
                road.prev_longitude = latitude
                road.matching = json.dumps({'coordinates': [
                    [longitude, latitude],
                    [longitude, latitude]]
                })

            print(road.matching)
            road.save()

