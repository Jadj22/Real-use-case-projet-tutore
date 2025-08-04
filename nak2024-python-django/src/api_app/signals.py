from django.db.models.signals import post_save
from django.dispatch import receiver
from web_app.models import Vendeur, Utilisateur, Client

from .forms import ValidatedToVendeur

@receiver(post_save, sender=Utilisateur)
def create_client(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil client pour chaque nouvel utilisateur.
    """
    if created:
        try:
            client = Client.objects.create(idutilisateur=instance)
            print(f"Client profile created for user {instance.username}")
        except Exception as e:
            print(f"Error creating client profile: {e}")

@receiver(post_save, sender=Utilisateur)
def create_vendeur(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil vendeur pour chaque nouvel utilisateur.
    Désactivé : le profil vendeur ne doit être créé que via le formulaire vendeur.
    """
    # if created:
    #     try:
    #         vendeur = Vendeur.objects.create(
    #             idutilisateur=instance,
    #             nom_boutique=f"Boutique de {instance.username}",
    #             statut_boutique="En cours de configuration",
    #             type_vendeur="Standard"
    #         )
    #         print(f"Seller profile created for user {instance.username}")
    #     except Exception as e:
    #         print(f"Error creating seller profile: {e}")
    pass

@receiver(post_save, sender=Utilisateur)
def validate_vendeur(sender, instance, created, **kwargs):
    """
    Valide les informations du vendeur si l'utilisateur est marqué comme vendeur.
    """
    if created:
        try:
            vendeur = Vendeur.objects.get(idutilisateur=instance)
            # Ici vous pouvez ajouter la logique de validation supplémentaire
            # par exemple, vérifier si certaines informations sont requises
            print(f"Seller profile validated for user {instance.username}")
        except Vendeur.DoesNotExist:
            print(f"No seller profile found for user {instance.username}")
        except Exception as e:
            print(f"Error validating seller profile: {e}")