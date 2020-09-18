from django import forms
#from django.forms import ModelForm
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import Dog


class DogCreationForm(forms.ModelForm):
    birthDate = forms.DateField(
        # input_formats=['%d/%m/%Y', ],
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'jj/mm/aaaa',
                # 'type': 'date',
                # 'value': datetime.now().strftime('%d/%m/%Y')
            })
    )

    class Meta:
        model = Dog
        fields = '__all__'
        exclude = (
            'hostFamily',
            'owner',
            'sponsor',
            'adopted',
            'hosted',
            'sponsored',
            'hasHostDemand',
            'hasAdoptionDemand',
        )

        labels = {
            'rabiesVaccines': _('Vaccins antirabiques'),
            'serology': _('Sérologie'),
            'name': _('Nom'),
            'sex': _('Sexe'),
            'dogBreed': _('Race'),
            'birthDate': _('Date de naissance'),
            'arrivalDate': _('Date d\'arrivée'),
            'dogCoat': _('Pelage'),
            'recognitionSigns': _('Signe(s) distinctif(s)'),
            'chipId': _('DogId (puce)'),
            'picture': _('Photo'),
            'size': _('Taille'),
            'story': _('Petite présentation'),
        }

        widgets = {
            'birthDate': forms.DateInput(format='%d/%m/%Y')
        }

        error_messages = {
            'name': {
                'max_length': _("Nom trop long."),
            },
        }

        help_texts = {}


    # birthDate = forms.DateField(input_formats=('%d/%m/%Y', ))
    # arrivalDate = forms.DateField(input_formats=('%d/%m/%Y', ))


class DogUpdateForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'
        exclude = (
            'sex',
            'dogBreed',
            'birthDate',
            'arrivalDate',
            'dogCoat',
            'chipId',
            'adopted',
            'hosted',
            'sponsored',
            'hasHostDemand',
            'hasAdoptionDemand',
        )

        labels = {
            'rabiesVaccines': _('Vaccins antirabiques'),
            'serology': _('Sérologie'),
            'name': _('Nom'),
            'recognitionSigns': _('Signe(s) distinctif(s)'),
            'picture': _('Photo'),
            'sponsor': _('Marraine/parrain'),
            'hostFamily': _('Famille d\'accueil'),
            'owner': _('Propriétaire'),
            'size': _('Taille'),
            'story': _('Petite présentation'),
        }

        error_messages = {
            'name': {
                'max_length': _("Nom trop long."),
            },
        }

        help_texts = {}