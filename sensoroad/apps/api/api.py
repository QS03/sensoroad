
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required

@login_required()
def upload_image(request):
    return JsonResponse(dict(
        success=True, message="image uploaded successfully"))
