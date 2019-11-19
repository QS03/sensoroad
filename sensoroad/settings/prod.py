from .base import *

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sensorydb',
        'USER': 'postgres',
        'PASSWORD': 'p8y8ei6F2HHKybut',
        'HOST': '172.27.160.3',
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/mnt/sensory/media'
