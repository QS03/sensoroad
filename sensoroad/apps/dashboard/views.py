from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect

# Create your views here.

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required


city_state_list =  ['San Francisco, Califonia', 'New York, New York', 'Los Angeles, Califonia', ]

def dashboard_view(request):
  if not request.user.is_authenticated:
    return redirect('login')

  sel_city_state = city_state_list[0]
  context = {'user': request.user, 'city_state_list': city_state_list, 'sel_city_state': sel_city_state}
  return render(request, 'dashboard.html', context)

def city_view(request, sel_city_state):
  if not request.user.is_authenticated:
    return redirect('login')

  context = {'user': request.user, 'city_state_list': city_state_list, 'sel_city_state': sel_city_state}
  return render(request, 'dashboard.html', context)
