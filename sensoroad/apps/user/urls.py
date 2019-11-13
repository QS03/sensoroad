from django.conf.urls import url, include

from . import views as users_views

urlpatterns = [
    url(r'login/', users_views.login, name='login'),
    url(r'signup/', users_views.signup, name='signup'),
]