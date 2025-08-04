from rest_framework import serializers
from web_app.models import Utilisateur, Vendeur

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'nom', 'prenom', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = Utilisateur.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            password=validated_data['password']
        )
        return user

class BecomeSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendeur
        fields = ['nom_boutique', 'adresse_boutique', 'type_vendeur', 'categorie', 'imagesproduits']
        extra_kwargs = {
            'statut_boutique': {'default': 'En cours de configuration'},
            'type_vendeur': {'default': 'Standard'},
        }

    def update(self, instance, validated_data):
        # Mettre à jour les informations du vendeur
        instance.nom_boutique = validated_data.get('nom_boutique', instance.nom_boutique)
        instance.adresse_boutique = validated_data.get('adresse_boutique', instance.adresse_boutique)
        instance.type_vendeur = validated_data.get('type_vendeur', instance.type_vendeur)
        instance.categorie = validated_data.get('categorie', instance.categorie)
        instance.imagesproduits = validated_data.get('imagesproduits', instance.imagesproduits)
        instance.statut_boutique = 'En cours de configuration'
        instance.save()
        return instance
