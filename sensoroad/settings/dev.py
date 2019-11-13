from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sensoroad',
        'USER': 'sensoroad',
        'PASSWORD': 'sensoroad',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}