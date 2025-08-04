from rest_framework import routers

from .viewset import AnnonceViewSet, VendeurViewSet

app_name = 'api_app'

rooter_api = routers.DefaultRouter()
rooter_api.register(r'annonce', AnnonceViewSet, basename='annonce')
rooter_api.register(r'vendeur', VendeurViewSet, basename='vendeur')


