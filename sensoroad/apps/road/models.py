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

    def get_object_for_dashboard(self, hostname):
        image_path = settings.MEDIA_URL + self.image.path.split(settings.MEDIA_URL)[1]
        data = {
            'image': image_path,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'point_rate': self.point_rate,
            'line_rate': self.line_rate,
            'street': self.street,
            'city': self.city,
            'state': self.state,
        }
        return data

    def get_object_for_rating(self):
        data = {
            'id': self.id,
            'previous_id': self.previous_id,
            'image': self.image.path,
            'longitude': self.longitude,
            'latitude': self.latitude,
        }
        return data

