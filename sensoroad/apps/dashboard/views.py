from django.shortcuts import render

# Create your views here.

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required


@login_required()
def dashboard_view(request):
    return JsonResponse(dict(
        success=True, message="dashboard loaded successfully"))
