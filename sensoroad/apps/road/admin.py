from django.contrib import admin

# Register your models here.
from .models import Road


class RoadAdmin(admin.ModelAdmin):
    model = Road
    list_display = ['id', 'user', 'image', 'longitude', 'latitude', 'taken_at', 'point_rate', 'line_rate', 'street', 'city', 'state']
    search_fields = ('street', 'city', 'state')


admin.site.register(Road, RoadAdmin)
