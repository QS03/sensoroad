from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sensoroad',
        'USER': 'postgres',
        'PASSWORD': 'p8y8ei6F2HHKybut',
        'HOST': '35.223.248.221',
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/mnt/sensory/media'