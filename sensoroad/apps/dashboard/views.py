from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect

# Create your views here.

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {'user': request.user}
    return render(request, 'dashboard.html', context)
