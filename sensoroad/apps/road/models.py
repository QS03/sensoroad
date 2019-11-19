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
        json = {
            'id': self.id,
            'previous_id': self.previous_id,
            'image': self.image.path,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'taken_at': self.taken_at,
            'device_id': self.user.username,
        }
        return json

    def get_object_for_dashboard(self):
        pass

    def get_object_for_rating(self):
        pass
