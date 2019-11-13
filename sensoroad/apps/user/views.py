from django.shortcuts import render

# Create your views here.


from django.http import Http404, JsonResponse


def login(request):
    return JsonResponse(dict(
        success=True, message="login successfully"))


def signup(request):
    return JsonResponse(dict(
        success=True, message="signup successfully"))