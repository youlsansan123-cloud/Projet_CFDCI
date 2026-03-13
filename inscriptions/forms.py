from django import forms
from .models import Etudiant, Formation, MessageContact


class EtudiantForm(forms.ModelForm):

    class Meta:
        model = Etudiant
        fields = [
            'nom',
            'prenom',
            'email',
            'telephone',
            'formation',  # ✅ AJOUT IMPORTANT
            'ville',
            'pays',
            'date_naissance',
            'numero_etudiant'
        ]

        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'telephone': 'Téléphone',
            'formation': 'Choisir une formation',
            'ville': 'Ville',
            'pays': 'Pays',
            'date_naissance': 'Date de naissance',
            'numero_etudiant': 'Numéro étudiant',
        }

    # ✅ Filtrer uniquement les formations actives
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['formation'].queryset = Formation.objects.filter(est_active=True)


class MessageContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_message(self):
        message = (self.cleaned_data.get('message') or '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Veuillez saisir au moins 10 caracteres.')
        return message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
