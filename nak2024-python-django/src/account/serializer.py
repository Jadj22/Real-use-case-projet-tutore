from django.contrib.auth.models import update_last_login
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

User = get_user_model()

class AbstractSerializer(ModelSerializer):
    public_id = serializers.UUIDField(read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

class AbstractViewSet(ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated', 'created']
    ordering = ['-updated']

class UserSerializer(AbstractSerializer):
    isSeller = serializers.SerializerMethodField()
    vendeur = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['public_id', 'username', 'email', 'nom', 'prenom', 'password', 'isSeller', 'vendeur']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def get_isSeller(self, obj):
        from web_app.models import Vendeur
        return Vendeur.objects.filter(idutilisateur=obj).exists()

    def get_vendeur(self, obj):
        from web_app.models import Vendeur
        vendeur = Vendeur.objects.filter(idutilisateur=obj).first()
        if vendeur:
            return {
                'nom_boutique': vendeur.nom_boutique,
                'adresse_boutique': vendeur.adresse_boutique,
                'type_vendeur': vendeur.type_vendeur,
                'categorie': vendeur.categorie,
                'imagesproduits': vendeur.imagesproduits,
            }
        return None

    def create(self, validated_data):
        """Créer un utilisateur avec un mot de passe hashé."""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Mettre à jour un utilisateur en gérant correctement le mot de passe."""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserRegisterSerializer(UserSerializer):
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'nom', 'prenom', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = RefreshToken.for_user(self.user)
        
        # Format des données pour le frontend
        response_data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        }
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        
        return response_data


class BecomeSellerSerializer(serializers.Serializer):
    nom_boutique = serializers.CharField(max_length=255, required=True)
    adresse_boutique = serializers.CharField(max_length=255, required=True)
    type_vendeur = serializers.CharField(max_length=50, required=True)
    categorie = serializers.CharField(max_length=100, required=True)
    imagesproduits = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('nom_boutique'):
            raise serializers.ValidationError({"nom_boutique": "Le nom de la boutique est requis"})
        if not data.get('adresse_boutique'):
            raise serializers.ValidationError({"adresse_boutique": "L'adresse est requise"})
        if not data.get('type_vendeur'):
            raise serializers.ValidationError({"type_vendeur": "Le type de vendeur est requis"})
        if not data.get('categorie'):
            raise serializers.ValidationError({"categorie": "La catégorie est requise"})
        return data