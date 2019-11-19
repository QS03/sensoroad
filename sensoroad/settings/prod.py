from .base import *

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sensorydb_test',
        'USER': 'postgres',
        'PASSWORD': 'sensorydb',
        'HOST': '172.27.160.3',
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/mnt/sensory/media'
