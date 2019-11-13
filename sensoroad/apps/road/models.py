from django.db import models
from django.db.models import Model
import uuid
# Create your models here.


class Road(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.IntegerField(blank=False)
    photo = models.ImageField(upload_to='image/', blank=False)
    longitude = models.FloatField(blank=False)
    latitude = models.FloatField(blank=False)
    taken_at = models.DateTimeField()
    street = models.TextField()
    rate = models.IntegerField()

    def __str__(self):
        return self.id
