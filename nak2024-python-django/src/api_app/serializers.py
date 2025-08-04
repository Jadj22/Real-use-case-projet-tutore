from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.serializer import AbstractSerializer
from web_app.models import Annonce, Vendeur, Client

User = get_user_model()


class AnnonceSerializer(AbstractSerializer):
    vendeur = serializers.PrimaryKeyRelatedField(queryset=Vendeur.objects.all())
    
    class Meta:
        model = Annonce
        fields = [
            'idannonce', 'vendeur', 'titre', 'description', 'categorie', 'prix',
            'photos', 'datepublication', 'statut', 'tags', 'stockproduit', 'contact',
            'public_id', 'created', 'updated'
        ]
        depth = 1  # Pour inclure les données du vendeur dans la réponse
        read_only_fields = ['idannonce', 'public_id', 'created', 'updated']

    def validate_idvendeur(self, value):
        """Valider que l'idvendeur appartient bien à l'utilisateur connecté."""
        user = self.context['request'].user
        if not Vendeur.objects.filter(idvendeur=value.idvendeur, idutilisateur=user.id).exists():
            raise ValidationError("Vous devez être un vendeur pour créer une annonce.")
        return value


class VendeurSerializer(AbstractSerializer):
    class Meta:
        model = Vendeur
        fields = [
            'idvendeur', 'idutilisateur', 'nom_boutique', 'adresse_boutique',
            'statut_boutique', 'type_vendeur', 'horaires', 'evaluation', 'produits',
            'categorie', 'imagesproduits', 'enligne', 'public_id', 'created', 'updated'
        ]
        read_only_fields = ['idvendeur', 'public_id', 'created', 'updated']

    def validate_idutilisateur(self, value):
        """Vérifier que l'utilisateur est le même que celui authentifié."""
        if value != self.context['request'].user.id:
            raise ValidationError("Vous ne pouvez pas créer un vendeur pour un autre utilisateur.")
        return value


class ClientSerializer(AbstractSerializer):
    class Meta:
        model = Client
        fields = ['idclient', 'idutilisateur', 'public_id', 'created', 'updated']
        read_only_fields = ['idclient', 'public_id', 'created', 'updated']
