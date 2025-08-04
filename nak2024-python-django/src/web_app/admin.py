from django.contrib import admin

from .models import Utilisateur, Vendeur, Client, Annonce, Favoris, Historique,Cartinteractive

# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Vendeur)
admin.site.register(Client)
admin.site.register(Annonce)
admin.site.register(Favoris)
admin.site.register(Historique)
admin.site.register(Cartinteractive)



