from django.urls import path, include
from .rooter import rooter_api
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

def block_models_request(request):
    return JsonResponse({'error': 'This route is not used.'}, status=404)

urlpatterns = [
    path('', include(rooter_api.urls)),
    path("v1/models", block_models_request),
]
