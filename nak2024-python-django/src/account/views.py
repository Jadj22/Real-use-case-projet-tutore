from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from account.serializer import UserLoginSerializer, BecomeSellerSerializer
from web_app.models import Vendeur

User = get_user_model()

class UserLoginView(APIView):
    permission_classes = []  # No authentication required for login
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BecomeSellerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = BecomeSellerSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data  # ✅ Déplacé ici

                try:
                    vendeur = Vendeur.objects.get(idutilisateur=request.user)
                    # Mise à jour
                    vendeur.nom_boutique = data.get('nom_boutique', vendeur.nom_boutique)
                    vendeur.adresse_boutique = data.get('adresse_boutique', vendeur.adresse_boutique)
                    vendeur.type_vendeur = data.get('type_vendeur', vendeur.type_vendeur)
                    vendeur.categorie = data.get('categorie', vendeur.categorie)
                    vendeur.imagesproduits = data.get('imagesproduits', vendeur.imagesproduits)
                    vendeur.save()

                    return Response({
                        'message': 'Votre profil vendeur a été mis à jour avec succès',
                        'data': {
                            'nom_boutique': vendeur.nom_boutique,
                            'adresse_boutique': vendeur.adresse_boutique,
                            'type_vendeur': vendeur.type_vendeur,
                            'categorie': vendeur.categorie,
                            'imagesproduits': vendeur.imagesproduits
                        }
                    }, status=status.HTTP_200_OK)

                except Vendeur.DoesNotExist:
                    # Création
                    vendeur = Vendeur.objects.create(
                        idutilisateur=request.user,
                        nom_boutique=data.get('nom_boutique', ''),
                        adresse_boutique=data.get('adresse_boutique', ''),
                        type_vendeur=data.get('type_vendeur', ''),
                        categorie=data.get('categorie', ''),
                        imagesproduits=data.get('imagesproduits', '')
                    )

                    return Response({
                        'message': 'Votre profil vendeur a été créé avec succès',
                        'data': {
                            'nom_boutique': vendeur.nom_boutique,
                            'adresse_boutique': vendeur.adresse_boutique,
                            'type_vendeur': vendeur.type_vendeur,
                            'categorie': vendeur.categorie,
                            'imagesproduits': vendeur.imagesproduits
                        }
                    }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ToggleUserRoleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            user.is_seller = not user.is_seller
            user.save()
            
            return Response({
                'message': 'Rôle mis à jour avec succès',
                'is_seller': user.is_seller
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, seller_id, *args, **kwargs):
        try:
            vendeur = Vendeur.objects.get(id=seller_id)
            return Response({
                'nom_boutique': vendeur.nom_boutique,
                'adresse_boutique': vendeur.adresse_boutique,
                'type_vendeur': vendeur.type_vendeur,
                'categorie': vendeur.categorie,
                'imagesproduits': vendeur.imagesproduits
            }, status=status.HTTP_200_OK)
            
        except Vendeur.DoesNotExist:
            return Response({'error': 'Vendeur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, seller_id, *args, **kwargs):
        try:
            vendeur = Vendeur.objects.get(id=seller_id)

            # Empêche un utilisateur de modifier une boutique qui n’est pas la sienne
            if vendeur.idutilisateur != request.user:
                return Response({'error': 'Non autorisé à modifier cette boutique.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = StoreUpdateSerializer(vendeur, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Vendeur.DoesNotExist:
            return Response({'error': 'Vendeur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)