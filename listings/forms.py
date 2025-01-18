from django import forms
from .models import Publication

class writePublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['message', 'picture', 'isPrivate']  # Champs à afficher dans le formulaire

    picture = forms.ImageField(required=False)