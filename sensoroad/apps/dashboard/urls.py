from django.conf.urls import url, include

from . import views as dashboard_views

urlpatterns = [
    url('', dashboard_views.dashboard_view, name='dashboard_view'),
]
