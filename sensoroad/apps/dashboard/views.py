from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

# Create your views here.

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from sensoroad.settings.base import MAPBOX_ACCESS_TOKEN
import json

from sensoroad.apps.road.models import Road
'''
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
]

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
]
'''

def dashboard_view(request):
  if not request.user.is_authenticated:
    return redirect('login')

  if request.user.member_type == 'mobile':
    return render_to_response('404.html')

  if request.user.member_type == 'user':
    city = request.user.city
    state = request.user.state
    sel_city_state = {'city': city, 'state': state}
    city_state_list = []

    points_data = []
    lines_data = []
    points = Road.objects.filter(city=city).filter(state=state)
    for point in points:
      res = point.get_object_for_dashboard()
      points_data.append(res['point_data'])
      lines_data.append(res['line_data'])

    context = {
      'city_state_list': city_state_list,
      'sel_city_state': sel_city_state,
      'points_data': json.dumps(points_data),
      'lines_data': json.dumps(lines_data),
      'mapbox_access_token': MAPBOX_ACCESS_TOKEN
    }
    return render(request, 'dashboard.html', context)

  if request.user.member_type == 'admin':
    points_data = []
    lines_data = []
    city_state_list = []
    points = Road.objects.exclude(city='').exclude(state='')
    for point in points:
      res = point.get_object_for_dashboard()
      points_data.append(res['point_data'])
      lines_data.append(res['line_data'])
      city_state_list.append({'city': point.city, 'state': point.state})

    city_state_list = [dict(t) for t in {tuple(city_state.items()) for city_state in city_state_list}]
    city = request.user.city
    state = request.user.state
    if city == '' or state == '':
      if len(city_state_list) > 0:
        sel_city_state = city_state_list[0]
      else:
        sel_city_state = {'city': city, 'state': state}
    else:
      sel_city_state = {'city': city, 'state': state}
      city_state_list.append({'city': city, 'state': state})

    context = {
      'city_state_list': city_state_list,
      'sel_city_state': sel_city_state,
      'points_data': json.dumps(points_data),
      'lines_data': json.dumps(lines_data),
      'mapbox_access_token': MAPBOX_ACCESS_TOKEN
    }
    return render(request, 'dashboard.html', context)


def city_view(request, city, state):
  if not request.user.is_authenticated:
    return redirect('login')

  if request.user.member_type != 'admin':
    return render_to_response('404.html')

  points_data = []
  lines_data = []
  points = Road.objects.filter(city=city).filter(state=state)
  for point in points:
    res = point.get_object_for_dashboard()
    points_data.append(res['point_data'])
    lines_data.append(res['line_data'])

  city_state_list = []
  points = Road.objects.exclude(city='').exclude(state='')
  for point in points:
    city_state_list.append({'city': point.city, 'state': point.state})

  city_state_list = [dict(t) for t in {tuple(city_state.items()) for city_state in city_state_list}]

  sel_city_state = {'city': city, 'state': state}
  if request.user.city != '' and request.user.state != '':
    city_state_list.append({'city': request.user.city, 'state': request.user.state})

  context = {
    'city_state_list': city_state_list,
    'sel_city_state': sel_city_state,
    'points_data': json.dumps(points_data),
    'lines_data': json.dumps(lines_data),
    'mapbox_access_token': MAPBOX_ACCESS_TOKEN
  }
  return render(request, 'dashboard.html', context)


def handler404(request, exception, template_name="404.html"):
  response = render_to_response("404.html")
  response.status_code = 404
  return response


def handler500(request, *args, **argv):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response