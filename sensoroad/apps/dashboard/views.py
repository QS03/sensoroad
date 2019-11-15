from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required


@login_required()
def dashboard_view(request):

    context = {'user': request.user}
    return render(request, 'dashboard.html', context)
