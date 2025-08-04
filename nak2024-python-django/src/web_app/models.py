
import uuid

from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractModel(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AbstractManager()

    class Meta:
        abstract = True

@deconstructible
class ProfilePathGenerator:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]  # Récupérer la dernière extension du fichier
        return f'media/accounts/{instance.id}/profile_image.{ext}'


profile_image = ProfilePathGenerator()


class UtilisateurManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Créer un utilisateur simple."""
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Créer un superutilisateur."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class Utilisateur(AbstractModel, AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    photoprofil = models.ImageField(blank=True, null=True, upload_to=profile_image)
    dateinscription = models.DateField(auto_now_add=True)  # Ajout automatique de la date
    localisation = models.JSONField(blank=True, null=True)
    numtelephone = models.CharField(max_length=20, blank=True, null=True)
    statutconnexion = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'username'  # Si tu veux utiliser l'email, remplace par 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        #managed = False
        db_table = 'utilisateur'


class Admin(models.Model):
    idadmin = models.AutoField(primary_key=True)
    idutilisateur = models.OneToOneField('Utilisateur', models.DO_NOTHING, db_column='idutilisateur')
    privileges = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'admin'


class Annonce(models.Model):
    idannonce = models.AutoField(primary_key=True)
    vendeur = models.ForeignKey('Vendeur', on_delete=models.CASCADE, related_name='annonces', null=True, blank=True)
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    prix = models.FloatField()
    photos = models.TextField(blank=True, null=True)  # This field type is a guess.
    datepublication = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    stockproduit = models.TextField(blank=True, null=True)  # This field type is a guess.
    contact = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'annonce'


class Cartinteractive(models.Model):
    idcart = models.AutoField(primary_key=True)
    idvendeur = models.ForeignKey('Vendeur', models.DO_NOTHING, db_column='idvendeur')

    class Meta:
        #managed = False
        db_table = 'cartinteractive'


class Client(models.Model):
    idclient = models.AutoField(primary_key=True)
    idutilisateur = models.OneToOneField('Utilisateur', models.DO_NOTHING, db_column='idutilisateur')

    class Meta:
        #managed = False
        db_table = 'client'

    def __str__(self):
        return  f'Utilisateur {self.idutilisateur}'


class Favoris(models.Model):
    idclient = models.OneToOneField(Client, models.DO_NOTHING, db_column='idclient',
                                    primary_key=True)  # The composite primary key (idclient, idannonce) found, that is not supported. The first column is selected.
    idannonce = models.ForeignKey(Annonce, models.DO_NOTHING, db_column='idannonce')
    dateajout = models.DateField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'favoris'
        unique_together = (('idclient', 'idannonce'),)


class Historique(models.Model):
    idclient = models.OneToOneField(Client, models.DO_NOTHING, db_column='idclient',
                                    primary_key=True)  # The composite primary key (idclient, idannonce) found, that is not supported. The first column is selected.
    idannonce = models.ForeignKey(Annonce, models.DO_NOTHING, db_column='idannonce')
    dateconsultation = models.DateField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'historique'
        unique_together = (('idclient', 'idannonce'),)

    def __str__(self):
        return f'historique de {self.idclient}'





class Vendeur(AbstractModel):
    idvendeur = models.AutoField(primary_key=True)
    idutilisateur = models.OneToOneField(Utilisateur, models.DO_NOTHING, db_column='idutilisateur')
    nom_boutique = models.CharField(max_length=255, blank=True, null=True)
    adresse_boutique = models.TextField(blank=True, null=True)
    statut_boutique = models.CharField(max_length=50, blank=True, null=True)
    type_vendeur = models.CharField(max_length=50, blank=True, null=True)
    horaires = models.TextField(blank=True, null=True)
    evaluation = models.FloatField(blank=True, null=True)
    produits = models.TextField(blank=True, null=True)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    imagesproduits = models.TextField(blank=True, null=True)  # This field type is a guess.
    enligne = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'vendeur'
