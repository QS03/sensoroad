from django.conf.urls import url, include

from . import api as api_views

urlpatterns = [
    url(r'^upload/?$', api_views.upload_image, name='upload_image'),
]