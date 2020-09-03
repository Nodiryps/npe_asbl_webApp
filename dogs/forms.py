from django import forms
from django.forms import ModelForm
from .models import Dog
from django.utils.translation import gettext_lazy as _


class DogCreationForm(ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'
        exclude = (
            'hostFamily',
            'owner',
            'sponsor',
            'adopted',
            'sponsored',
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

        error_messages = {
            'name': {
                'max_length': _("Nom trop long."),
            },
        }

        help_texts = {}


    # birthDate = forms.DateField(input_formats=('%d/%m/%Y', ))
    # arrivalDate = forms.DateField(input_formats=('%d/%m/%Y', ))


class DogUpdateForm(ModelForm):
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