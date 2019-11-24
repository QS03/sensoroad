import uuid
from django.db import models
from django.conf import settings
# Create your models here.


class Road(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    previous_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', blank=False)
    longitude = models.FloatField(blank=False)
    latitude = models.FloatField(blank=False)
    taken_at = models.DateTimeField(blank=True, null=True)
    point_rate = models.IntegerField(blank=True, null=True)
    line_rate = models.IntegerField(blank=True, null=True)
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
            point_rate = 0
        else:
            point_rate = int(self.point_rate)

        try:
            previous_road = Road.objects.get(pk=self.previous_id)

            if previous_road.point_rate is None:
                previous_point_rate = point_rate
            else:
                previous_point_rate = int(previous_road.point_rate)

            previous_point = {
                'longitude': previous_road.longitude,
                'latitude': previous_road.latitude,
            }
        except Road.DoesNotExist:
            previous_point = {
                'longitude': self.longitude,
                'latitude': self.latitude,
            }
            previous_point_rate = point_rate

        point_data = {
             'coordinate': [self.longitude, self.latitude],
             'rate': point_rate,
             'image_url': image_path
         }

        line_data = {
            'coordinates': [
                [self.longitude, self.latitude],
                [previous_point['longitude'], previous_point['latitude']],
            ],
            'rate': int((point_rate + previous_point_rate)/2)
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

