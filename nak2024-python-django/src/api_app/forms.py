from django import forms


class ValidatedToVendeur(forms.Form):
    vendeur = forms.BooleanField(disabled=True)
