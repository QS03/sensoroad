from .base import *

from .base import *

HOST_ADDRESS = '172.27.160.3'
HOST_NAME = 'dashboard.sensory.city'
MOBILE_HOST = 'mobile.sensory.city'

ALLOWED_HOSTS = [HOST_ADDRESS, HOST_NAME, MOBILE_HOST]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sensorydb',
        'USER': 'sensory',
        'PASSWORD': 'p8y8ei6F2HHKybut',
        'HOST': HOST_ADDRESS,
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/mnt/sensory/media'
