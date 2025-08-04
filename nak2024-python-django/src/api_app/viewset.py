from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.serializer import AbstractViewSet
from web_app.models import Annonce, Vendeur, Client
from .serializers import AnnonceSerializer, VendeurSerializer, ClientSerializer


class AnnonceViewSet(ModelViewSet):
    serializer_class = AnnonceSerializer
    queryset = Annonce.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]  # GET autorisé à tous
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        print(f"[DEBUG] Headers de la requête: {dict(self.request.headers)}")
        print(f"[DEBUG] Paramètres de requête: {dict(self.request.query_params)}")
        
        queryset = Annonce.objects.all()
        idvendeur = self.request.query_params.get('idvendeur')
        
        print(f"[DEBUG] Avant filtrage - Nombre total d'annonces: {queryset.count()}")
        print(f"[DEBUG] Paramètre idvendeur reçu: {idvendeur} (type: {type(idvendeur)})")
        
        if idvendeur:
            try:
                # Essayer de convertir en entier
                idvendeur_int = int(idvendeur)
                print(f"[DEBUG] Filtrage avec idvendeur={idvendeur_int}")
                queryset = queryset.filter(idvendeur=idvendeur_int)
                print(f"[DEBUG] Après filtrage - Nombre d'annonces: {queryset.count()}")
                
                # Vérifier si des annonces ont été trouvées
                if queryset.count() == 0:
                    print("[DEBUG] Aucune annonce trouvée pour ce vendeur")
                    # Vérifier si le vendeur existe
                    from web_app.models import Vendeur
                    if not Vendeur.objects.filter(idvendeur=idvendeur_int).exists():
                        print(f"[DEBUG] Le vendeur avec l'ID {idvendeur_int} n'existe pas")
                    else:
                        print(f"[DEBUG] Le vendeur {idvendeur_int} existe mais n'a pas d'annonces")
                
            except ValueError as e:
                print(f"[DEBUG] Erreur de conversion de l'ID vendeur: {e}")
                # Retourner un queryset vide si l'ID n'est pas un nombre valide
                return Annonce.objects.none()
        else:
            print("[DEBUG] Aucun paramètre idvendeur fourni, retour de toutes les annonces")
        
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retrieve the current user's announcements
        """
        user = request.user
        
        if not hasattr(user, 'vendeur'):
            return Response(
                {"detail": "Seuls les vendeurs ont des annonces."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get the vendeur's ID
        vendeur_id = user.vendeur.idvendeur
        
        # Filter announcements by the current vendeur using vendeur_id field
        queryset = self.get_queryset().filter(vendeur_id=vendeur_id)
        
        # Paginate the results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Vous devez être authentifié."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not hasattr(user, 'vendeur'):
            return Response(
                {"detail": "Seuls les vendeurs peuvent créer des annonces."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the Vendeur instance for the current user
        vendeur_instance = user.vendeur
        
        # Copy the request data and set the vendeur instance
        data = request.data.copy()
        data['idvendeur'] = vendeur_instance.idvendeur  # This will be converted to Vendeur instance by the serializer

        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VendeurViewSet(AbstractViewSet, ModelViewSet):
    serializer_class = VendeurSerializer
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Vendeur.objects.all()

    def get_object(self):
        obj = Vendeur.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']


class ClientList(ReadOnlyModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [AllowAny]
