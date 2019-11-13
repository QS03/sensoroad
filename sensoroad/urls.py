"""sensoroad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # This needs to be added
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from sensoroad.apps.api import urls as api_urls
from sensoroad.apps.user.views import login, signup
from sensoroad.apps.dashboard.views import dashboard_view

urlpatterns = [
    path('accounts/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('^api/', include(api_urls)),

    url('^$', dashboard_view, name='dashboard'),
    url('^dashboard/$', dashboard_view, name='dashboard'),
    url('^login/$', login, name='login'),
    url('^signup/$', signup, name='signup'),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
