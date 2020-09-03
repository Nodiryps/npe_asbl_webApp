from django import forms
from .models import Post
from dogs.models import Dog
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', 'timestamp')

        dog = forms.ModelChoiceField(
            queryset=Dog.objects.filter(adopted=True),
            empty_label=Dog.objects.filter(adopted=True)[0],
            # to_field_name='name'
        )

        labels = {
            'dog': _('Nom du loulou'),
            'body': _('Petite déscription'),
            'postPicture': _('Photo'),
        }


    def getUserDogs():
        # users = User.objects.filter()
        return Dog.objects.filter(adopted=True)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostCreationForm, self).__init__(*args, **kwargs)
        self.fields['dog'].queryset = Dog.objects.filter(adopted=True, owner=self.user) | Dog.objects.filter(hosted=True, hostFamily=self.user)