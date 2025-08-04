from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Annonce
from .serializers import AnnonceSerializer
from .permissions import IsVendeurPermission

class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [IsVendeurPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendeur', 'categorie', 'statut']
    search_fields = ['titre', 'description', 'tags']
    ordering_fields = ['prix', 'datepublication']

    def get_queryset(self):
        # Vérifier que l'utilisateur est authentifié
        if not self.request.user.is_authenticated:
            return queryset.none()

        queryset = super().get_queryset()
        public_id = self.request.query_params.get('public_id')
        
        # Si aucun public_id n'est fourni, retourner uniquement les annonces de l'utilisateur connecté
        if not public_id:
            try:
                vendeur = Vendeur.objects.get(idutilisateur=self.request.user.id)
                queryset = queryset.filter(vendeur=vendeur)
            except Vendeur.DoesNotExist:
                return queryset.none()
        else:
            try:
                vendeur = Vendeur.objects.get(public_id=public_id)
                queryset = queryset.filter(vendeur=vendeur)
            except Vendeur.DoesNotExist:
                return queryset.none()  # Retourne un queryset vide si le vendeur n'existe pas
        
        # Exclure les annonces sans vendeur
        queryset = queryset.exclude(vendeur__isnull=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(vendeur=self.request.user.vendeur)
