from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect

# Create your views here.

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from sensoroad.settings.base import MAPBOX_ACCESS_TOKEN
import json

city_state_list =  ['San Francisco, Califonia', 'New York, New York', 'Los Angeles, Califonia']

points_data = [
  {'coordinate': [-122.4833858013153, 37.829607404976734], 'rate': 1, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.4830961227417, 37.82932776098012], 'rate': 3, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48339653015138, 37.83270036637107], 'rate': 2, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48356819152832, 37.832056363179625], 'rate': 5, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48404026031496, 37.83114119107971], 'rate': 6, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48404026031496, 37.83049717427869], 'rate': 7, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48348236083984, 37.829920943955045], 'rate': 10, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48356819152832, 37.82954808664175], 'rate': 4, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48507022857666, 37.82944639795659], 'rate': 7, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48610019683838, 37.82880236636284], 'rate': 9, 'image_url': "static/assets/img/test.jpg"},
  {'coordinate': [-122.48695850372314, 37.82931081282506], 'rate': 9, 'image_url': "static/assets/img/test.jpg"}
];

lines_data = [
  {'coordinates': [[-122.4833858013153, 37.829607404976734], [-122.4830961227417, 37.82932776098012]], 'rate': 2},
  {'coordinates': [[-122.4830961227417, 37.82932776098012], [-122.48339653015138, 37.83270036637107]], 'rate': 3},
  {'coordinates': [[-122.48339653015138, 37.83270036637107], [-122.48356819152832, 37.832056363179625]], 'rate': 5},
  {'coordinates': [[-122.48356819152832, 37.832056363179625], [-122.48404026031496, 37.83114119107971]], 'rate': 1},
  {'coordinates': [[-122.48404026031496, 37.83114119107971], [-122.48404026031496, 37.83049717427869]], 'rate': 8},
  {'coordinates': [[-122.48404026031496, 37.83049717427869], [-122.48348236083984, 37.829920943955045]], 'rate': 9},
  {'coordinates': [[-122.48348236083984, 37.829920943955045], [-122.48356819152832, 37.82954808664175]], 'rate': 4},
  {'coordinates': [[-122.48356819152832, 37.82954808664175], [-122.48507022857666, 37.82944639795659]], 'rate': 10},
  {'coordinates': [[-122.48507022857666, 37.82944639795659], [-122.48610019683838, 37.82880236636284]], 'rate': 7},
  {'coordinates': [[-122.48610019683838, 37.82880236636284], [-122.48695850372314, 37.82931081282506]], 'rate': 6}
];

def dashboard_view(request):
  if not request.user.is_authenticated:
    return redirect('login')

  sel_city_state = city_state_list[0]

  context = {'user': request.user, 'city_state_list': city_state_list, 'sel_city_state': sel_city_state,
             'points_data': json.dumps(points_data), 'lines_data': json.dumps(lines_data), 'mapbox_access_token': MAPBOX_ACCESS_TOKEN}
  return render(request, 'dashboard.html', context)

def city_view(request, sel_city_state):
  if not request.user.is_authenticated:
    return redirect('login')

  context = {'user': request.user, 'city_state_list': city_state_list, 'sel_city_state': sel_city_state,
             'points_data': json.dumps(points_data), 'lines_data': json.dumps(lines_data), 'mapbox_access_token': MAPBOX_ACCESS_TOKEN}
  return render(request, 'dashboard.html', context)
